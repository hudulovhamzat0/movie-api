let searchTimeout;
let suggestionTimeout;
let isSearched = false;

const searchBox = document.getElementById('searchBox');
const container = document.getElementById('container');
const logo = document.getElementById('logo');
const resultsContainer = document.getElementById('resultsContainer');
const results = document.getElementById('results');
const loading = document.getElementById('loading');
const noResults = document.getElementById('noResults');
const suggestions = document.getElementById('suggestions');
const resultsHeader = document.getElementById('resultsHeader');
const stats = document.getElementById('stats');

// Stats yükle
fetch('/api/stats')
  .then(response => response.json())
  .then(data => {
    stats.innerHTML = `📊 ${data.total_documents?.toLocaleString()} kayıt`;
  })
  .catch(() => {
    stats.innerHTML = '📊 Database bağlı değil';
  });

// Search box focus event
searchBox.addEventListener('focus', () => {
  if (!isSearched) {
    setTimeout(() => {
      container.classList.add('searched');
      logo.classList.add('searched');
      isSearched = true;
    }, 100);
  }
});

// Canlı arama
searchBox.addEventListener('input', (e) => {
  const query = e.target.value.trim();

  clearTimeout(searchTimeout);
  clearTimeout(suggestionTimeout);

  if (query.length < 2) {
    hideResults();
    hideSuggestions();
    return;
  }

  // Öneriler için kısa timeout
  suggestionTimeout = setTimeout(() => {
    fetchSuggestions(query);
  }, 200);

  // Arama için uzun timeout
  searchTimeout = setTimeout(() => {
    performSearch(query);
  }, 500);
});

// Öneriler için fetch
function fetchSuggestions(query) {
  fetch(`/api/suggestions?q=${encodeURIComponent(query)}`)
    .then(response => response.json())
    .then(data => {
      showSuggestions(data.suggestions || []);
    })
    .catch(err => {
      console.error('Suggestions error:', err);
    });
}

// Önerileri göster
function showSuggestions(suggestionsList) {
  if (suggestionsList.length === 0) {
    hideSuggestions();
    return;
  }

  suggestions.innerHTML = suggestionsList
    .map(s => `<div class="suggestion-item" onclick="selectSuggestion('${s.replace(/'/g, "\\'")}')">${s}</div>`)
    .join('');

  suggestions.style.display = 'block';
}

// Öneri seçildiğinde
function selectSuggestion(suggestion) {
  searchBox.value = suggestion;
  hideSuggestions();
  performSearch(suggestion);
}

// Önerileri gizle
function hideSuggestions() {
  suggestions.style.display = 'none';
}

// Click outside to hide suggestions
document.addEventListener('click', (e) => {
  if (!e.target.closest('.search-container')) {
    hideSuggestions();
  }
});

// Arama yap
function performSearch(query) {
  showLoading();
  hideResults();
  hideSuggestions();

  fetch(`/api/search?q=${encodeURIComponent(query)}`)
    .then(response => response.json())
    .then(data => {
      hideLoading();
      if (data.results && data.results.length > 0) {
        showResults(data.results, data.total, query);
      } else {
        showNoResults();
      }
    })
    .catch(err => {
      hideLoading();
      console.error('Search error:', err);
      showNoResults();
    });
}

// Sonuçları göster
function showResults(resultsList, total, query) {
  resultsHeader.innerHTML = `"${query}" için yaklaşık ${total.toLocaleString()} sonuç bulundu`;

  results.innerHTML = resultsList.map(item => {
    let title, info, description;

    // title.basics formatı
    if (item.primaryTitle) {
      title = item.primaryTitle;
      info = [
        item.titleType && `<span class="info-badge">${item.titleType}</span>`,
        item.startYear && `<span class="info-badge">${item.startYear}</span>`,
        item.runtimeMinutes && `<span class="info-badge">${item.runtimeMinutes} dk</span>`
      ].filter(Boolean).join('');

      description = [
        item.originalTitle !== item.primaryTitle ? `Orijinal adı: ${item.originalTitle}` : null,
        item.genres ? `Türler: ${item.genres}` : null
      ].filter(Boolean).join(' • ');
    }
    // name.basics formatı
    else if (item.primaryName) {
      title = item.primaryName;
      info = [
        item.primaryProfession && `<span class="info-badge">${item.primaryProfession}</span>`,
        item.birthYear && `<span class="info-badge">${item.birthYear}</span>`
      ].filter(Boolean).join('');

      description = [
        item.knownForTitles ? `Bilinen işleri: ${item.knownForTitles}` : null
      ].filter(Boolean).join(' • ');
    }
    else {
      title = 'Bilinmeyen';
      info = '';
      description = JSON.stringify(item, null, 2);
    }

    return `
      <div class="result-item">
        <div class="result-title">${title}</div>
        <div class="result-info">${info}</div>
        <div class="result-description">${description}</div>
      </div>
    `;
  }).join('');

  resultsContainer.classList.add('visible');
  noResults.classList.remove('visible');
}

// Sonuç yok
function showNoResults() {
  hideResults();
  noResults.classList.add('visible');
}

// Loading göster
function showLoading() {
  loading.classList.add('visible');
}

// Loading gizle
function hideLoading() {
  loading.classList.remove('visible');
}

// Sonuçları gizle
function hideResults() {
  resultsContainer.classList.remove('visible');
  noResults.classList.remove('visible');
}

// Enter tuşu desteği
searchBox.addEventListener('keypress', (e) => {
  if (e.key === 'Enter') {
    const query = e.target.value.trim();
    if (query.length >= 2) {
      clearTimeout(searchTimeout);
      clearTimeout(suggestionTimeout);
      performSearch(query);
    }
  }
});
