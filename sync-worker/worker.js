// Abgleich für die 4-Blocks-Karte: Geräte mit demselben geheimen Sync-Code teilen
// einen Index (Szenen + eigene Drehorte) und die Szenenbilder (JPEG).
const ORIGINS = ['https://oehmm.github.io', 'http://localhost:8795', 'http://localhost:8796'];
const MAX_INDEX = 512 * 1024, MAX_IMG = 4 * 1024 * 1024;

export default {
  async fetch(req, env) {
    const origin = req.headers.get('Origin') || '';
    const cors = {
      'Access-Control-Allow-Origin': ORIGINS.includes(origin) ? origin : ORIGINS[0],
      'Access-Control-Allow-Methods': 'GET,PUT,DELETE,OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type',
      'Access-Control-Max-Age': '86400',
      'Vary': 'Origin',
    };
    const json = (body, status = 200) => new Response(JSON.stringify(body), { status, headers: { ...cors, 'Content-Type': 'application/json', 'Cache-Control': 'no-store' } });
    if (req.method === 'OPTIONS') return new Response(null, { headers: cors });

    const m = new URL(req.url).pathname.match(/^\/v1\/([a-z0-9]{20,64})\/(?:index|img\/([a-z0-9-]{6,64}))$/);
    if (!m) return json({ error: 'not_found' }, 404);
    const [, code, img] = m;
    const key = img ? `s:${code}:img:${img}` : `s:${code}:index`;

    if (req.method === 'GET') {
      if (img) {
        const v = await env.KV.get(key, 'arrayBuffer');
        if (!v) return json({ error: 'not_found' }, 404);
        return new Response(v, { headers: { ...cors, 'Content-Type': 'image/jpeg', 'Cache-Control': 'private, max-age=31536000, immutable' } });
      }
      const v = await env.KV.get(key);
      return new Response(v || '{}', { headers: { ...cors, 'Content-Type': 'application/json', 'Cache-Control': 'no-store' } });
    }
    if (req.method === 'PUT') {
      const buf = await req.arrayBuffer();
      if (buf.byteLength > (img ? MAX_IMG : MAX_INDEX)) return json({ error: 'too_large' }, 413);
      if (img) {
        const b = new Uint8Array(buf, 0, Math.min(3, buf.byteLength));
        if (!(b[0] === 0xFF && b[1] === 0xD8)) return json({ error: 'unsupported_type' }, 415);
      } else {
        try { const o = JSON.parse(new TextDecoder().decode(buf)); if (!o || typeof o !== 'object' || Array.isArray(o)) throw 0; }
        catch { return json({ error: 'invalid_json' }, 400); }
      }
      await env.KV.put(key, buf);
      return json({ ok: true });
    }
    if (req.method === 'DELETE' && img) { await env.KV.delete(key); return json({ ok: true }); }
    return json({ error: 'method_not_allowed' }, 405);
  },
};
