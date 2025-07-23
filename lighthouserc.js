module.exports = {
  ci: {
    collect: {
      url: [
        'http://localhost:4000',
        'http://localhost:4000/cv/',
        'http://localhost:4000/publications/',
        'http://localhost:4000/projects/'
      ],
      settings: {
        chromeFlags: '--no-sandbox'
      }
    },
    assert: {
      assertions: {
        'categories:performance': ['warn', { minScore: 0.8 }],
        'categories:accessibility': ['error', { minScore: 0.9 }],
        'categories:best-practices': ['warn', { minScore: 0.8 }],
        'categories:seo': ['error', { minScore: 0.9 }]
      }
    },
    upload: {
      target: 'temporary-public-storage'
    }
  }
};
