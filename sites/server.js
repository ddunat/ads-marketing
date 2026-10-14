// DC Building Inspectors landing pages. Leads go to GHL (inbound webhook) and Meta CAPI.
const http = require('http'), fs = require('fs'), path = require('path'), crypto = require('crypto');
const PUB = path.join(__dirname, 'public');
const { PORT = 3000, GHL_WEBHOOK_URL, LEAD_EMAIL_WEBHOOK_URL, META_PIXEL_ID, META_CAPI_TOKEN, GHL_BOOKING_URL, BOOKING_LINK = 'https://dcinspect.com.au/online-bookings', META_TEST_EVENT_CODE, BOOKING_TOKEN, GHL_BOOKING_WEBHOOK_URL } = process.env;
// One entry per ad landing page. key = GHL tag + Meta content name; hot = stage answers routed to /thankyou-book.
const LANDERS = {
  '/auction': { file: 'auction.html', key: 'lp-a2-auction', ad: 'A2 auction', service: 'pre-purchase', hot: /Auction|Signed/ },
};
const PAGES = { '/thankyou': 'thankyou.html', '/thankyou-book': 'thankyou-book.html' };
for (const [p, l] of Object.entries(LANDERS)) PAGES[p] = l.file;
const TYPES = { '.webp': 'image/webp', '.mp4': 'video/mp4', '.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.svg': 'image/svg+xml', '.ico': 'image/x-icon' };

const pixel = META_PIXEL_ID ? `<script>!function(f,b,e,v,n,t,s){if(f.fbq)return;n=f.fbq=function(){n.callMethod?n.callMethod.apply(n,arguments):n.queue.push(arguments)};if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}(window,document,'script','https://connect.facebook.net/en_US/fbevents.js');fbq('init','${META_PIXEL_ID}');fbq('track','PageView');</script>` : '';
// Lead fires on both thank-you pages (Jeremy), with the same event_id as CAPI so Meta de-duplicates.
const leadJs = META_PIXEL_ID ? `<script>(function(){var e=new URLSearchParams(location.search).get('e');if(e&&window.fbq)fbq('track','Lead',{},{eventID:e});})();</script>` : '';
// Embedded GHL calendar if set, otherwise a button to the website's online booking page.
const booking = GHL_BOOKING_URL ? `<iframe src="${GHL_BOOKING_URL}" title="Book your inspection" loading="lazy"></iframe>`
  : `<a class="go" href="${BOOKING_LINK}?utm_source=meta&utm_medium=lp&utm_campaign=thankyou-book">Book online now →</a>`;

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
  const lander = LANDERS[clean(d.page)];
  if (!lander) return send(res, 400, { ok: false });
  const hot = lander.hot.test(clean(d.stage));
  const lead = {
    first_name, phone: mobile.replace(/^0/, '+61'), email,
    property_type: clean(d.property_type), bedrooms: clean(d.bedrooms), stage: clean(d.stage), suburb: clean(d.suburb),
    lead_temp: hot ? 'hot' : 'warm', service: lander.service, landing_page: lander.key,
    tags: ['meta-lead', lander.key, lander.service, hot ? 'hot' : 'warm'],
    source: `Meta ad: ${lander.ad}`, page: clean(d.page), event_id: clean(d.event_id),
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
      custom_data: { lead_temp: lead.lead_temp, content_name: lander.key } }] };
    if (META_TEST_EVENT_CODE) ev.test_event_code = META_TEST_EVENT_CODE;
    post(`https://graph.facebook.com/v21.0/${META_PIXEL_ID}/events?access_token=${META_CAPI_TOKEN}`, ev).catch(e => console.error('CAPI failed:', e.message.replace(META_CAPI_TOKEN, '***')));
  }
  send(res, 200, { ok: true, hot });
}

// GoDaddy Online Appointments "Booking Confirmed" email (relayed by Zapier from Gmail) -> Meta Schedule + GHL "booked".
const grab = (t, re) => (t.match(re) || [])[1]?.trim() || '';
function parseBooking(t) {
  const name = grab(t, /Name:\s*\n\s*(.+)/), [fn, ...ln] = name.split(/\s+/);
  const where = grab(t, /Where:\s*\n([\s\S]*?)\n\s*\n/);
  return {
    order: grab(t, /Order #\s*(C-[A-Z0-9]+)/), total: parseFloat(grab(t, /Order Total \$([\d,.]+)/).replace(/,/g, '')) || 0,
    first_name: fn || '', last_name: ln.join(' '), phone: grab(t, /Phone:\s*\n\s*([+\d ]+)/).replace(/\s/g, ''), email: grab(t, /Email:\s*\n\s*(\S+@\S+)/),
    service: grab(t, /What:\s*\n\s*(.+)/), when: grab(t, /When:\s*\n\s*(.+)/), payment: grab(t, /Payment status:\s*\n\s*(.+)/),
    suburb: grab(where, /\n\s*(.+?)\s+VIC/i), postcode: grab(where, /VIC\s+(\d{4})/i),
  };
}
async function handleBooking(req, res) {
  if (!BOOKING_TOKEN || req.headers['x-booking-token'] !== BOOKING_TOKEN) return send(res, 401, { ok: false });
  let raw = ''; for await (const c of req) { raw += c; if (raw.length > 100000) return send(res, 413, { ok: false }); }
  let d; try { d = JSON.parse(raw); } catch { return send(res, 400, { ok: false }); }
  if (!/Booking Confirmed/.test(d.subject || '')) return send(res, 200, { ok: true, skipped: 'not a booking' });
  const b = parseBooking(String(d.body || ''));
  if (!b.order || !(b.email || b.phone)) return send(res, 422, { ok: false });
  const phone = b.phone.replace(/^0/, '+61'), jobs = [];
  if (GHL_BOOKING_WEBHOOK_URL) jobs.push(post(GHL_BOOKING_WEBHOOK_URL, { ...b, phone, source: 'GoDaddy online booking' }));
  if (META_PIXEL_ID && META_CAPI_TOKEN) {
    const ev = { data: [{ event_name: 'Schedule', event_time: Math.floor(Date.now() / 1000), event_id: `booking-${b.order}`, action_source: 'website',
      event_source_url: 'https://dcinspect.com.au/online-bookings',
      user_data: { em: [sha(b.email)], ph: [sha(phone.replace('+', ''))], fn: [sha(b.first_name)], ln: [sha(b.last_name)],
        ct: [sha(b.suburb.replace(/\s/g, ''))], zp: [sha(b.postcode)], country: [sha('au')] },
      custom_data: { value: b.total, currency: 'AUD', content_name: b.service, order_id: b.order } }] };
    if (META_TEST_EVENT_CODE) ev.test_event_code = META_TEST_EVENT_CODE;
    jobs.push(post(`https://graph.facebook.com/v21.0/${META_PIXEL_ID}/events?access_token=${META_CAPI_TOKEN}`, ev));
  }
  const r = await Promise.allSettled(jobs);
  r.filter(x => x.status === 'rejected').forEach(x => console.error('booking relay failed:', String(x.reason.message).replace(META_CAPI_TOKEN || '~', '***')));
  console.log('booking', b.order, 'relayed', r.filter(x => x.status === 'fulfilled').length, '/', jobs.length);
  send(res, 200, { ok: true, order: b.order });
}

function send(res, code, obj) { res.writeHead(code, { 'Content-Type': 'application/json' }); res.end(JSON.stringify(obj)); }

http.createServer((req, res) => {
  const url = new URL(req.url, 'http://x');
  const p = url.pathname.replace(/\/+$/, '') || '/';
  if (req.method === 'POST' && p === '/api/lead') return handleLead(req, res).catch(e => { console.error(e); send(res, 500, { ok: false }); });
  if (req.method === 'POST' && p === '/api/booking') return handleBooking(req, res).catch(e => { console.error(e); send(res, 500, { ok: false }); });
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
