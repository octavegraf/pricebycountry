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
                const span = document.createElement('span');

                const url = new URL(file.Url);
                const domain = url.hostname;

                const fileNameWithoutExtension = file.Path.split('/').pop().replace('.json', '');

                a.href = `subscription/?file=${fileNameWithoutExtension}`;
                span.className = 'subscription-list__text-button';
                span.textContent = file.Name;

                a.appendChild(span);
                li.appendChild(a);
                ul.appendChild(li);
            });

            listSection.appendChild(ul);
        })
        .catch(error => console.error('Error loading subscription list:', error));
});
