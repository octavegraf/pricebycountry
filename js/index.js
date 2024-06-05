document.addEventListener('DOMContentLoaded', () => {
    fetch('subscriptions_list.json')
        .then(response => response.json())
        .then(data => {
            const listSection = document.querySelector('.subscriptions-list');
            const ul = document.createElement('ul');
            ul.className = 'subscription-list__ul';

            data.Subscriptions.forEach(file => {
                const li = document.createElement('li');
                const a = document.createElement('a');
                const img = document.createElement('img');

                const url = new URL(file.Url);
                const domain = url.hostname;

                const fileNameWithoutExtension = file.Path.split('/').pop().replace('.json', '');

                a.href = `subscription.html?file=${fileNameWithoutExtension}`;
                img.src = `https://logo.clearbit.com/${domain}`;
                img.alt = `${file.Name} logo`;
                a.appendChild(img);
                a.appendChild(document.createTextNode(file.Name));

                li.appendChild(a);
                ul.appendChild(li);
            });

            listSection.appendChild(ul);
        })
        .catch(error => console.error('Error loading subscription list:', error));
});
