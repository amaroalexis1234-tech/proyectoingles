/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,

  allowedDevOrigins: [
    "192.168.1.26",
    "localhost",
    "127.0.0.1",
  ],
};

module.exports = nextConfig;