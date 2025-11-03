# Frontend - Full Stack Developer Assessment

Written by Rahul M — internship assessment project

This React + TypeScript frontend presents imaginary analytics charts (similar theme to superbryn.com).
- Uses Vite + React + TypeScript
- Uses Recharts for charts
- Collects user email before allowing overwriting of chart data
- Stores custom values in Supabase (client side). .env variables are required.
- When user tries to update values and previous values exist, the app shows a confirmation dialog.

Dev notes:
- For demo, set up a free Supabase project and copy `SUPABASE_URL` and `SUPABASE_ANON_KEY` into `.env.local`.
- The app includes a small debug console.log in `src/dev-utils.ts`.

Run locally:
PS> cd frontend
PS> npm install
PS> npm run dev
