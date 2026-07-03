// Set your site password hash (SHA-256 hex). Generate with:
//   node -e "const c=require('crypto');console.log(c.createHash('sha256').update('YOUR_PASSWORD').digest('hex'))"
window.SITE_CONFIG = {
  passwordHash: "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8",
  authKey: "portfolio_auth_v1",
};
