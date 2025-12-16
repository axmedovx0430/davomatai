/** @type {import('next').NextConfig} */
const nextConfig = {
  images: {
    domains: ['localhost'],
  },
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || '',
  },
  // Memory optimization
  webpack: (config, { dev, isServer }) => {
    // Disable webpack cache in development to prevent memory issues
    if (dev) {
      config.cache = false;
    }

    // Memory optimization
    config.optimization = {
      ...config.optimization,
      minimize: !dev,
      splitChunks: false,
    };

    return config;
  },
  // Reduce concurrent builds
  experimental: {
    workerThreads: false,
    cpus: 1,
  },
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'http://127.0.0.1:8080/api/:path*',
      },
    ]
  },
}

module.exports = nextConfig
