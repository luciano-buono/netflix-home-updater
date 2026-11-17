// Cloudflare Email Worker bound to netflix@<domain>.
// Fans out each Netflix email to the personal inbox and the SendGrid
// Inbound Parse address. Both must be verified Email Routing destinations.
const NETFLIX_SENDER = "@account.netflix.com";

export default {
  async email(message, env) {
    const from = (message.headers.get("from") || "").toLowerCase();
    const targets = [env.PERSONAL_INBOX];
    if (from.includes(NETFLIX_SENDER)) {
      targets.push(env.CHECKER_INBOX);
    }

    const results = await Promise.allSettled(targets.map((to) => message.forward(to)));
    const failed = results.filter((r) => r.status === "rejected");
    for (const r of failed) {
      console.error(`forward failed: ${r.reason}`);
    }
    if (failed.length === targets.length) {
      message.setReject("Forwarding failed");
    }
  },
};
