/** @type {import('next').NextConfig} */
const nextConfig = {
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
  },
  // Disable strict mode to avoid double rendering in development
  reactStrictMode: false,
}

module.exports = nextConfig
