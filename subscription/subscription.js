document.addEventListener('DOMContentLoaded', () => {
    const params = new URLSearchParams(window.location.search);
    const fileParam = params.get('file');

    if (!fileParam) {
        console.error('No file parameter provided.');
        return;
    }

    const fileName = `../data/${fileParam}.json`;
    const exchangeRatesFile = '../exchange_rates.json';
    const countriesFile = '../countries.json';

    Promise.all([
        fetch(exchangeRatesFile).then(response => response.json()),
        fetch(fileName).then(response => response.json()),
        fetch(countriesFile).then(response => response.json())
    ])
    .then(([exchangeRates, data, countries]) => {
        const infosSection = document.querySelector('.infos');
        const pricesSection = document.querySelector('.prices');

        const domain = new URL(data.Url).hostname;
        const logoUrl = `https://logo.clearbit.com/${domain}`;
        const name = data.Name;
        const url = data.Url.replace(/^https?:\/\/(www\.)?/, '');

        document.title = `PriceByCountry - ${name}`;

        const metaDescription = document.createElement('meta');
        metaDescription.name = 'description';
        metaDescription.content = `You can find the price for ${name} in every country.`;
        document.head.appendChild(metaDescription);

        const logo = infosSection.querySelector('.infos__logo');
        logo.src = logoUrl;
        logo.alt = `${name} Logo`;

        const h1 = infosSection.querySelector('.infos__h1');
        h1.textContent = name;

        const link = infosSection.querySelector('.infos__link');
        link.href = data.Url;
        link.textContent = url;

        const offers = [];
        data.Offers.forEach(offerType => {
            for (const [offerName, offerDetails] of Object.entries(offerType)) {
                offerDetails.forEach(detail => {
                    const priceInEur = detail.Currency === 'EUR' 
                        ? detail.Price 
                        : detail.Price / exchangeRates.conversion_rates[detail.Currency];
                    offers.push({
                        offerName,
                        country: detail.Country,
                        price: priceInEur
                    });
                });
            }
        });

        const groupedOffers = offers.reduce((acc, offer) => {
            if (!acc[offer.offerName]) {
                acc[offer.offerName] = [];
            }
            acc[offer.offerName].push(offer);
            return acc;
        }, {});

        const countryLookup = countries.reduce((acc, country) => {
            acc[country.code.toLowerCase()] = `${country.emoji} ${country.name}`;
            return acc;
        }, {});

        for (const [offerName, offerDetails] of Object.entries(groupedOffers)) {
            offerDetails.sort((a, b) => a.price - b.price);

            const card = document.createElement('div');
            card.className = 'prices__card';

            const h2 = document.createElement('h2');
            h2.className = 'prices__h2';
            h2.textContent = offerName;

            const table = document.createElement('table');
            table.className = 'prices__table';

            const headerRow = document.createElement('tr');
            const headerCountry = document.createElement('th');
            headerCountry.textContent = '🏳️ Country';
            const headerPrice = document.createElement('th');
            headerPrice.textContent = 'Price';
            headerRow.appendChild(headerCountry);
            headerRow.appendChild(headerPrice);
            table.appendChild(headerRow);

            offerDetails.forEach(detail => {
                const row = document.createElement('tr');
                const countryCell = document.createElement('td');
                countryCell.textContent = countryLookup[detail.country.toLowerCase()] || detail.country;
                const priceCell = document.createElement('td');
                priceCell.textContent = `${detail.price.toFixed(2)}€`;
                row.appendChild(countryCell);
                row.appendChild(priceCell);
                table.appendChild(row);
            });

            card.appendChild(h2);
            card.appendChild(table);
            pricesSection.appendChild(card);
        }
    })
    .catch(error => console.error('Error loading files:', error));
});
