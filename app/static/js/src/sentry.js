import * as Sentry from "@sentry/browser";
import { BrowserTracing } from "@sentry/tracing";

Sentry.init({
  dsn: "https://6bf317cfb9ec49409c8031da1942b68c@o457759.ingest.sentry.io/6103324",
  integrations: [new BrowserTracing(), new Sentry.Replay()],


  // Set tracesSampleRate to 1.0 to capture 100%
  // of transactions for performance monitoring.
  // We recommend adjusting this value in production
  tracesSampleRate: 1.0,

  // This sets the sample rate to be 10%. You may want this to be 100% while
  // in development and sample at a lower rate in production
  replaysSessionSampleRate: 0,
  // If the entire session is not sampled, use the below sample rate to sample
  // sessions when an error occurs.
  replaysOnErrorSampleRate: 1.0,
});

const memberName = document.querySelector('meta[name="sentry-member-name"]').content
const memberId = document.querySelector('meta[name="sentry-member-id"]').content

Sentry.setUser({ user_id: memberId, username: memberName });
