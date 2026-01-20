document.addEventListener('DOMContentLoaded', () => {
    const keywordInput = document.getElementById('keyword-input');
    const addKeywordBtn = document.getElementById('add-keyword-btn');
    const keywordsList = document.getElementById('keywords-list');
    const locationInput = document.getElementById('location-input');
    const searchArticlesBtn = document.getElementById('search-articles-btn');
    const articlesList = document.getElementById('articles-list');

    const API_URL = 'http://127.0.0.1:8000';

    async function fetchKeywords() {
        try {
            const response = await fetch(`${API_URL}/keywords`);
            const keywords = await response.json();
            keywordsList.innerHTML = '';
            keywords.forEach(keyword => {
                const li = document.createElement('li');
                li.textContent = keyword.value;
                keywordsList.appendChild(li);
            });
        } catch (error) {
            console.error('Error fetching keywords:', error);
        }
    }

    async function addKeyword() {
        const value = keywordInput.value.trim();
        if (value) {
            try {
                await fetch(`${API_URL}/keywords?value=${value}`, { method: 'POST' });
                keywordInput.value = '';
                fetchKeywords();
            } catch (error) {
                console.error('Error adding keyword:', error);
            }
        }
    }

    async function fetchArticlesByLocation() {
        const location = locationInput.value.trim();
        if (location) {
            try {
                const response = await fetch(`${API_URL}/articles/by-location?location=${location}`);
                const articles = await response.json();
                articlesList.innerHTML = '';
                articles.forEach(article => {
                    const li = document.createElement('li');
                    li.innerHTML = `
                        <h3>${article.title}</h3>
                        <p>${article.text}</p>
                        <p><strong>Keywords:</strong> ${article.keywords.join(', ')}</p>
                        <div><strong>Locations:</strong></div>
                        <ul>
                            ${article.locations.map(loc => `
                                <li>${loc.name} (${loc.latitude}, ${loc.longitude})</li>
                            `).join('')}
                        </ul>
                    `;
                    articlesList.appendChild(li);
                });
            } catch (error) {
                console.error('Error fetching articles:', error);
            }
        }
    }

    addKeywordBtn.addEventListener('click', addKeyword);
    searchArticlesBtn.addEventListener('click', fetchArticlesByLocation);

    fetchKeywords();
});
