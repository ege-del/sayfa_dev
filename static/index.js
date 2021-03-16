// created_category_doms = {}
function gen_category(target_dom,category){
    // created_category_doms[category] = true;
    console.log('gen category ',category);
    let buffer = $("#category-prot").clone();
    buffer.show();
    buffer.removeAttr('id');
    buffer.find('.news_category').text(category);
    buffer.find('.table_body').attr('id',category);
    $(target_dom).append(buffer);
  }
 
  function render_rank_dropdowns(){
    rank_dropdown_data.forEach(x => {
      console.log('append ',x)
      $('#rank_dropdown_menu').append(
      `<div data-value='${x.value}' class="item">
        <i class="${x.icon} icon"></i>
        ${x.text}
      </div>`);
    });
  }
  
  function format_date(date){
      var delta = Math.abs(new Date() - Date.parse(date)) / 1000;
      // calculate (and subtract) whole days
      var days = Math.floor(delta / 86400);
      delta -= days * 86400;
      // calculate (and subtract) whole hours
      var hours = Math.floor(delta / 3600) % 24;
      delta -= hours * 3600;
      // calculate (and subtract) whole minutes
      var minutes = Math.floor(delta / 60) % 60;
      delta -= minutes * 60;
      if(days > 0){
          return days.toString()+" Days Ago";
      }else if (hours > 0){
          return hours.toString()+" Hours Ago";
      }else{
          return minutes.toString()+" Minutes Ago";
      }
  }
  
  function gen_news_dom(data){
    return `
    <tr>
      <td class="top aligned collapsing">${data.domain}</td>
      <td><a href="${data.url}">${data.title}</a></td>
      <td class="top aligned collapsing">${format_date(data.date)}</td>
    </tr>
    `
  }
  
  function add_news(category,data){
    $('#'+category).append(gen_news_dom(data));
  }
  
  const urlParams = new URLSearchParams(window.location.search);
  
  function api_get_category(){
    return $.ajax({
          type: "GET",
          url: "http://127.0.0.1:1337/api/category",
          contentType: "application/json; charset=utf-8",
    })
  }

  //can repeat the query for pages in the future
  let q_category = "";
  let q_fetch = "";
  let q_rank_algorithm = "";
  let q_reverse_order = "";

  function api_get_news(q_type,data = null){
    if(q_type == "url"){
        q_category        =  urlParams.get('category');
        q_fetch           =  urlParams.get('fetch');
        q_rank_algorithm  =  urlParams.get('rank_algorithm');
        q_reverse_order   =  urlParams.get('reverse_order');
    }else if(q_type == 'direct'){
        q_category        = data[0];
        q_fetch           = data[1];
        q_rank_algorithm  = data[2];
        q_reverse_order   = data[3];
    }else if(q_type == 'field'){
        q_category        = $("#category_dropdown").dropdown('get value');
        q_fetch           = $('#fetch_ammount_dropdown').dropdown('get value');
        q_rank_algorithm  = $('#rank_algorithm_dropdown').dropdown('get value');
        q_reverse_order   = $('#reverse_checkbox').checkbox('is checked') == true ? "yes" : "no";
        console.log(q_reverse_order);
    }else{
        throw Error('unknown type')
    }

    // force sync. maybe dumb...
    $("#category_dropdown").dropdown('set selected',q_category.split(','));
    $('#fetch_ammount_dropdown').dropdown('set selected',q_fetch);
    $('#rank_algorithm_dropdown').dropdown('set selected',q_rank_algorithm);
    
    if(q_reverse_order == "yes"){
      $('#reverse_checkbox').checkbox('set checked');
    }else{
      $('#reverse_checkbox').checkbox('set unchecked');
    }
 

    let query_url = new URLSearchParams();
        
    query_url.set('category',q_category);
    query_url.set('fetch',q_fetch);
    query_url.set('rank_algorithm',q_rank_algorithm);
    query_url.set('reverse_order',q_reverse_order);

    setCookie('category',q_category,365);
    setCookie('fetch',q_fetch,365);
    setCookie('rank_algorithm',q_rank_algorithm,365);
    setCookie('reverse_order',q_reverse_order,365);
    

    window.history.pushState('Query','','news?'+query_url.toString());
    
    $('#content_h').empty();
    $.ajax({
          type: "GET",
          url: "http://127.0.0.1:1337/api/news"+window.location.search,
          contentType: "application/json; charset=utf-8",
      }).done((done_res)=>{
        console.log(done_res);
        if(done_res.data){
          Object.keys(done_res.data).forEach(key => {
            gen_category('#content_h',key);
            done_res.data[key].forEach(element => {
              add_news(element.category,element);
            });
          })
        }else{}
    });
  }
  
  function setCookie(name,value,days) {
      var expires = "";
      if (days) {
          var date = new Date();
          date.setTime(date.getTime() + (days*24*60*60*1000));
          expires = "; expires=" + date.toUTCString();
      }
      document.cookie = name + "=" + (value || "")  + expires + "; path=/";
  }
  function getCookie(name) {
      var nameEQ = name + "=";
      var ca = document.cookie.split(';');
      for(var i=0;i < ca.length;i++) {
          var c = ca[i];
          while (c.charAt(0)==' ') c = c.substring(1,c.length);
          if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
      }
      return null;
  }
  function eraseCookie(name) {   
      document.cookie = name +'=; Path=/; Expires=Thu, 01 Jan 1970 00:00:01 GMT;';
  }
  
  let category_list = [];
  let select_categories = [];
  
$(document).ready(function() {
    api_get_category().done((done_res)=>{
        if(done_res.data){
            category_list = done_res.data;
            console.log(category_list);
            $("#category_dropdown").dropdown(
                {
                    values:category_list.map(x => { return {name:x,value:x}}),
                }
            );
        }else{

        }
    }).then(()=>{
        console.log('CATEGORY CREATED');

        // $("#category_dropdown").dropdown('setting', 'action', function(a,b){
        //     console.log('CALLBACK ',a,b);
        //     api_get_news('field');
        // });

        if(window.location.search == ""){
          let a = getCookie('category');
          let b = getCookie('fetch');
          let c = getCookie('rank_algorithm');
          let d = getCookie('reverse_order');
            if(a && b && c && d){
              api_get_news('direct',[a,b,c,d]);
            }else{
              api_get_news('direct',['genetics,neuroscience',"5","newest","yes"]);
            }
        }else{
            api_get_news('url');
        }
        render_rank_dropdowns();
        $('.tabular.menu .item').tab();
    });
});