const title_link = document.getElementById('row');

fetch("../static/news_data.json")
 .then(res => res.json())
    .then(data => {

      const a = data;
      //console.log(a);
      const sortByDate = a => {
        const sorter = (a, b) => {
           return new Date(b.date).getTime() - new Date(a.date).getTime();
        }
        a.sort(sorter);
     };
     sortByDate(a);
     console.log(a);

     data.forEach(post => {

            if(post.category == "economy"){
                title_link.insertAdjacentHTML("beforeend" , `
                <div class="col-md-4">
                 <div class="card mb-4 box-shadow ">
                 <img class="card-img-top" src="${post.pic}" height="200px width="270" alt="Card image cap">
                <div class="card-body">
                  <p id="kaki" class="card-text ">${post.title}</p>
                  <div class="d-flex justify-content-between align-items-center">
                    <div class="btn-group">
                    <a id="btn" href="${post.link}" target="_blank"> <button type="button" class="btn btn-sm btn-outline-secondary">View More</button></a>

                    </div>
                    <small class="text-muted">${post.date}</small>
                  </div>
                </div>
              </div>
            </div>`);
 }
          });

       });