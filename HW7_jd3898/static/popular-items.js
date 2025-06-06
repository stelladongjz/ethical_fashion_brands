document.addEventListener('DOMContentLoaded', function () {
    const popularItems = JSON.parse(document.getElementById('popular-items-data').textContent);
    const container = document.getElementById("popular-items");

    popularItems.forEach(item => {
        let div = document.createElement("div");
        div.classList.add("col-md-4");
        div.innerHTML = `<div class="card">
            <div class="card-body">
                <h4 class="card-title"><a href="/view/${item.id}">${item.title}</a></h4>
            </div>
        </div>`;
        container.appendChild(div);
    });
});