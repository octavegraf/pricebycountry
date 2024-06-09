document.addEventListener('DOMContentLoaded', () => {
    const params = new URLSearchParams(window.location.search);
    const fileParam = params.get('file');

    if (!fileParam) {
        console.error('No file parameter provided.');
        return;
    }

    const fileName = `../data/${fileParam}.json`;
    const exchangeRatesFile = '../exchange_rates.json';

    fetch(exchangeRatesFile)
        .then(response => response.json())
        .then(exchangeRates => {
            fetch(fileName)
                .then(response => response.json())
                .then(data => {
                    const infosSection = document.querySelector('.infos');
                    const pricesSection = document.querySelector('.prices');

                    const domain = new URL(data.Url).hostname;
                    const logoUrl = `https://logo.clearbit.com/${domain}`;
                    const name = data.Name;
                    const url = data.Url.replace(/^https?:\/\/(www\.)?/, ''); // Remove http://, https://, and www.

                    document.title = `PriceByCountry - ${name}`;

                    const logo = infosSection.querySelector('.infos__logo');
                    logo.src = logoUrl;
                    logo.alt = `${name} Logo`;

                    const h1 = infosSection.querySelector('.infos__h1');
                    h1.textContent = name;

                    const link = infosSection.querySelector('.infos__link');
                    link.href = data.Url; // Keep the original URL for the href attribute
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
                        headerCountry.textContent = 'Country';
                        const headerPrice = document.createElement('th');
                        headerPrice.textContent = 'Price';
                        headerRow.appendChild(headerCountry);
                        headerRow.appendChild(headerPrice);
                        table.appendChild(headerRow);

                        offerDetails.forEach(detail => {
                            const row = document.createElement('tr');
                            const countryCell = document.createElement('td');
                            countryCell.textContent = detail.country.toUpperCase();
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
                .catch(error => console.error('Error loading subscription file:', error));
        })
        .catch(error => console.error('Error loading exchange rates file:', error));
});
