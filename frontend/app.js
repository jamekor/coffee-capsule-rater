const api = '';
let currentUser = null;

function show(id) {
  document.querySelectorAll('main .view').forEach(v => v.hidden = true);
  document.getElementById(id).hidden = false;
}

function loadCapsules() {
  fetch(api + '/capsules')
    .then(r => r.json())
    .then(data => {
      const list = document.getElementById('capsule-list');
      list.innerHTML = '';
      data.forEach(c => {
        const li = document.createElement('li');
        const link = document.createElement('a');
        link.textContent = c.name + ' (' + (c.average_rating ?? 'n/a') + ')';
        link.href = '#';
        link.onclick = (e) => {
          e.preventDefault();
          showCapsule(c.id);
        };
        li.appendChild(link);
        list.appendChild(li);
      });
    });
}

function showCapsule(id) {
  fetch(`${api}/capsules/${id}`)
    .then(r => r.json())
    .then(c => {
      document.getElementById('capsule-detail-name').textContent = c.name;
      document.getElementById('capsule-detail-brand').textContent = `Brand: ${c.brand}`;
      document.getElementById('capsule-detail-roast').textContent = `Roast: ${c.roast_level}`;
      document.getElementById('capsule-detail-flavor').textContent = `Flavor: ${c.flavor_notes}`;
      document.getElementById('capsule-detail-average').textContent = c.average_rating ?? 'n/a';
      loadRatings(id);
      show('capsule-detail-section');
      document.getElementById('rating-form').onsubmit = (ev) => {
        ev.preventDefault();
        if (!currentUser) { alert('Login required'); return; }
        const form = ev.target;
        const value = parseInt(form.value.value, 10);
        if (isNaN(value) || value < 1 || value > 5) { alert('Invalid rating'); return; }
        fetch(`${api}/capsules/${id}/ratings`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', 'X-User-ID': currentUser.id },
          body: JSON.stringify({ value: value, review: form.review.value })
        }).then(() => {
          form.reset();
          loadRatings(id);
          loadCapsules();
        });
      };
    });
}

function loadRatings(id) {
  fetch(`${api}/capsules/${id}/ratings`)
    .then(r => r.json())
    .then(rs => {
      const ul = document.getElementById('capsule-ratings');
      ul.innerHTML = '';
      rs.forEach(r => {
        const li = document.createElement('li');
        li.textContent = `${r.value}/5 - ${r.review}`;
        ul.appendChild(li);
      });
    });
}

document.getElementById('add-capsule-form').onsubmit = e => {
  e.preventDefault();
  const f = e.target;
  fetch(api + '/capsules', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      name: f.name.value,
      brand: f.brand.value,
      roast_level: f.roast_level.value,
      flavor_notes: f.flavor_notes.value
    })
  }).then(() => { f.reset(); loadCapsules(); show('capsules-section'); });
};

document.getElementById('signup-form').onsubmit = e => {
  e.preventDefault();
  const f = e.target;
  fetch(api + '/users', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username: f.username.value, email: f.email.value, password: f.password.value })
  }).then(r => r.json()).then(u => {
    currentUser = u;
    show('capsules-section');
  });
};

document.getElementById('login-form').onsubmit = e => {
  e.preventDefault();
  const f = e.target;
  fetch(api + '/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username: f.username.value, password: f.password.value })
  }).then(r => r.json()).then(u => {
    currentUser = u;
    loadProfile();
    show('capsules-section');
  });
};

function loadProfile() {
  if (!currentUser) return;
  const f = document.getElementById('profile-form');
  f.username.value = currentUser.username;
  f.email.value = currentUser.email;
}

document.getElementById('profile-form').onsubmit = e => {
  e.preventDefault();
  if (!currentUser) { alert('Login required'); return; }
  const f = e.target;
  fetch(`${api}/users/${currentUser.id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json', 'X-User-ID': currentUser.id },
    body: JSON.stringify({ username: f.username.value, email: f.email.value })
  }).then(r => r.json()).then(u => {
    currentUser = u;
    alert('Updated!');
  });
};

['nav-capsules', 'nav-add', 'nav-profile', 'nav-login', 'nav-signup'].forEach(id => {
  document.getElementById(id).onclick = (e) => {
    e.preventDefault();
    const map = {
      'nav-capsules': 'capsules-section',
      'nav-add': 'add-capsule-section',
      'nav-profile': 'profile-section',
      'nav-login': 'login-section',
      'nav-signup': 'signup-section'
    };
    show(map[id]);
  };
});

document.getElementById('capsule-search').oninput = e => {
  const term = e.target.value.toLowerCase();
  document.querySelectorAll('#capsule-list li').forEach(li => {
    li.style.display = li.textContent.toLowerCase().includes(term) ? '' : 'none';
  });
};

loadCapsules();
show('capsules-section');
