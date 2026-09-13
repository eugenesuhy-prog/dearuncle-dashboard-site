exports.handler = async (event) => {
  const params = event.queryStringParameters || {};
  const code = params.code || '';
  const state = params.state || '';
  if (!code) {
    return { statusCode: 400, headers: {'content-type':'text/html; charset=utf-8'}, body: '<h1>카페24 OAuth callback</h1><p>code가 없습니다. 승인 URL에서 다시 시작하세요.</p>' };
  }
  // The one-time authorization code is intentionally shown only to the operator.
  // Token exchange is performed separately so client secrets never appear in this page.
  return { statusCode: 200, headers: {'content-type':'text/html; charset=utf-8', 'cache-control':'no-store'}, body: `<!doctype html><meta charset="utf-8"><title>Cafe24 OAuth 승인 완료</title><style>body{font-family:system-ui;max-width:760px;margin:40px auto;padding:0 20px}code{display:block;background:#f3f4f6;padding:16px;word-break:break-all;border-radius:8px}</style><h1>카페24 OAuth 승인 완료</h1><p>이 페이지를 닫지 말고 디어효신에게 “승인 완료”라고 알려주세요. 아래 인증 코드는 일회용이며 1분 후 만료됩니다.</p><code>${escapeHtml(code)}</code><p>state: <code>${escapeHtml(state)}</code></p>` };
};
function escapeHtml(value) { return String(value).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c])); }
