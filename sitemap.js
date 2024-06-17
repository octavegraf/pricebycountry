const fs = require('fs');
const path = require('path');
const axios = require('axios');

const subscriptionsUrl = 'https://octavegraf.github.io/pricebycountry/subscriptions_list.json';

const baseUrl = 'https://octavegraf.github.io/pricebycountry';

const generateSitemap = async () => {
  try {
    const response = await axios.get(subscriptionsUrl);
    const subscriptions = response.data.Subscriptions;
    let sitemap = `<?xml version="1.0" encoding="UTF-8"?>\n`;
    sitemap += `<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n`;

    subscriptions.forEach(subscription => {
      const fileName = path.basename(subscription.Path, '.json');
      const url = `${baseUrl}?file=${fileName}`;
      sitemap += `  <url>\n`;
      sitemap += `    <loc>${url}</loc>\n`;
      sitemap += `  </url>\n`;
    });

    sitemap += `</urlset>\n`;

    fs.writeFileSync(path.join(__dirname, 'sitemap.xml'), sitemap);
    console.log('Sitemap generated successfully!');
  } catch (error) {
    console.error('Error generating sitemap:', error);
  }
};

generateSitemap();