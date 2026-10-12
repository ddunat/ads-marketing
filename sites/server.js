// DC Building Inspectors landing pages. Leads go to GHL (inbound webhook) and Meta CAPI.
const http = require('http'), fs = require('fs'), path = require('path'), crypto = require('crypto');
const PUB = path.join(__dirname, 'public');
const { PORT = 3000, GHL_WEBHOOK_URL, LEAD_EMAIL_WEBHOOK_URL, META_PIXEL_ID, META_CAPI_TOKEN, GHL_BOOKING_URL, META_TEST_EVENT_CODE } = process.env;
const PAGES = { '/auction': 'auction.html', '/thankyou': 'thankyou.html', '/thankyou-book': 'thankyou-book.html' };
const TYPES = { '.webp': 'image/webp', '.mp4': 'video/mp4', '.png': 'image/png', '.jpg': 'image/jpeg', '.svg': 'image/svg+xml', '.ico': 'image/x-icon' };
const HOT = /Auction|Signed/;

const pixel = META_PIXEL_ID ? `<script>!function(f,b,e,v,n,t,s){if(f.fbq)return;n=f.fbq=function(){n.callMethod?n.callMethod.apply(n,arguments):n.queue.push(arguments)};if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}(window,document,'script','https://connect.facebook.net/en_US/fbevents.js');fbq('init','${META_PIXEL_ID}');fbq('track','PageView');</script>` : '';
// Lead fires on both thank-you pages (Jeremy), with the same event_id as CAPI so Meta de-duplicates.
const leadJs = META_PIXEL_ID ? `<script>(function(){var e=new URLSearchParams(location.search).get('e');if(e&&window.fbq)fbq('track','Lead',{},{eventID:e});})();</script>` : '';
const booking = GHL_BOOKING_URL ? `<iframe src="${GHL_BOOKING_URL}" title="Book your inspection" loading="lazy"></iframe>` : `<a class="go" href="tel:+61483936872">Call 0483 936 872 to book</a>`;

const cache = {};
function page(file) {
  if (!cache[file]) cache[file] = fs.readFileSync(path.join(PUB, file), 'utf8')
    .replace('<!--PIXEL-->', pixel).replace('<!--LEAD-->', leadJs).replace('<!--BOOKING-->', booking);
  return cache[file];
}
const sha = v => v ? crypto.createHash('sha256').update(String(v).trim().toLowerCase()).digest('hex') : undefined;
const clean = v => String(v ?? '').slice(0, 200);

async function post(url, body) {
  const r = await fetch(url, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) });
  if (!r.ok) throw new Error(`${url.split('?')[0]} -> ${r.status} ${await r.text().catch(() => '')}`);
}

async function handleLead(req, res) {
  let raw = '';
  for await (const c of req) { raw += c; if (raw.length > 20000) return send(res, 413, { ok: false }); }
  let d; try { d = JSON.parse(raw); } catch { return send(res, 400, { ok: false }); }
  const mobile = clean(d.mobile).replace(/[\s()-]/g, ''), email = clean(d.email), first_name = clean(d.first_name);
  if (!first_name || !/^(\+?61|0)4\d{8}$/.test(mobile) || !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) return send(res, 422, { ok: false });
  const hot = HOT.test(clean(d.stage));
  const lead = {
    first_name, phone: mobile.replace(/^0/, '+61'), email,
    property_type: clean(d.property_type), bedrooms: clean(d.bedrooms), stage: clean(d.stage), suburb: clean(d.suburb),
    lead_temp: hot ? 'hot' : 'warm', tags: ['meta-lead', 'lp-a2-auction', hot ? 'hot' : 'warm'],
    source: 'Meta ad: A2 auction', page: clean(d.page), event_id: clean(d.event_id),
    utm_source: clean(d.utm_source), utm_medium: clean(d.utm_medium), utm_campaign: clean(d.utm_campaign), utm_content: clean(d.utm_content), fbclid: clean(d.fbclid),
    submitted_at: new Date().toISOString(),
  };
  const jobs = [];
  if (GHL_WEBHOOK_URL) jobs.push(post(GHL_WEBHOOK_URL, lead).then(() => 'ghl'));
  if (LEAD_EMAIL_WEBHOOK_URL) jobs.push(post(LEAD_EMAIL_WEBHOOK_URL, lead).then(() => 'email'));
  const results = await Promise.allSettled(jobs);
  const delivered = results.filter(r => r.status === 'fulfilled').length;
  results.filter(r => r.status === 'rejected').forEach(r => console.error('lead delivery failed:', r.reason.message));
  if (!delivered) { console.error('LEAD NOT DELIVERED', JSON.stringify({ ...lead, phone: '[redacted]', email: '[redacted]' })); return send(res, 502, { ok: false }); }
  if (META_PIXEL_ID && META_CAPI_TOKEN) {
    const ip = (req.headers['x-forwarded-for'] || '').split(',')[0].trim() || req.socket.remoteAddress;
    const ev = { data: [{ event_name: 'Lead', event_time: Math.floor(Date.now() / 1000), event_id: lead.event_id, action_source: 'website',
      event_source_url: `https://${req.headers.host}${lead.page}`,
      user_data: { em: [sha(email)], ph: [sha(lead.phone.replace('+', ''))], fn: [sha(first_name)], ct: [sha(lead.suburb.replace(/\s/g, ''))], country: [sha('au')],
        client_ip_address: ip, client_user_agent: req.headers['user-agent'], fbp: clean(d.fbp) || undefined, fbc: clean(d.fbc) || undefined },
      custom_data: { lead_temp: lead.lead_temp } }] };
    if (META_TEST_EVENT_CODE) ev.test_event_code = META_TEST_EVENT_CODE;
    post(`https://graph.facebook.com/v21.0/${META_PIXEL_ID}/events?access_token=${META_CAPI_TOKEN}`, ev).catch(e => console.error('CAPI failed:', e.message.replace(META_CAPI_TOKEN, '***')));
  }
  send(res, 200, { ok: true, hot });
}

function send(res, code, obj) { res.writeHead(code, { 'Content-Type': 'application/json' }); res.end(JSON.stringify(obj)); }

http.createServer((req, res) => {
  const url = new URL(req.url, 'http://x');
  const p = url.pathname.replace(/\/+$/, '') || '/';
  if (req.method === 'POST' && p === '/api/lead') return handleLead(req, res).catch(e => { console.error(e); send(res, 500, { ok: false }); });
  if (p === '/health') return send(res, 200, { ok: true });
  if (p === '/') { res.writeHead(302, { Location: 'https://dcinspect.com.au' }); return res.end(); }
  if (PAGES[p]) { res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8', 'Cache-Control': 'no-cache' }); return res.end(page(PAGES[p])); }
  if (p.startsWith('/img/')) {
    const f = path.join(PUB, path.normalize(p).replace(/^(\.\.[\/\\])+/, ''));
    if (f.startsWith(PUB) && fs.existsSync(f)) {
      const st = fs.statSync(f), type = TYPES[path.extname(f)] || 'application/octet-stream', range = req.headers.range;
      const h = { 'Content-Type': type, 'Cache-Control': 'public, max-age=604800', 'Accept-Ranges': 'bytes' };
      if (range) { // video seeking on iOS needs range requests
        const [s, e] = range.replace('bytes=', '').split('-'), start = +s, end = e ? +e : st.size - 1;
        res.writeHead(206, { ...h, 'Content-Range': `bytes ${start}-${end}/${st.size}`, 'Content-Length': end - start + 1 });
        return fs.createReadStream(f, { start, end }).pipe(res);
      }
      res.writeHead(200, { ...h, 'Content-Length': st.size }); return fs.createReadStream(f).pipe(res);
    }
  }
  res.writeHead(404, { 'Content-Type': 'text/plain' }); res.end('Not found');
}).listen(PORT, () => console.log('listening on', PORT));
