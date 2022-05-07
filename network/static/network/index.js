          document.addEventListener('DOMContentLoaded',function(){
                btn_list=document.querySelectorAll('button');
                btn_list.forEach(editPost);
                edit_list=document.querySelectorAll('a');
                edit_list.forEach(showLike);


function showLike(item){

   item.onclick=function(){
   like_counts=document.getElementById(item.id+'likes');
   console.log(item.id);
   btn_txt=item.innerText;
   if (item.id==""){
   console.log('error');
   }
   else{
   parent_a=document.getElementById(item.id);
   child_p=parent_a.getElementsByClassName("testp")[0]
  console.log('correct');
   fetch(`/likePost/${item.id}`, {
  method: 'PUT',
  body: JSON.stringify({
      like: true
  })
})

.then(response => {ret_resp=response.status;
if (ret_resp==204){
//item.innerHTML=response.btn_status
fetch(`/likePost/${item.id}`)
.then(response => response.json())
.then(data => {
  like_counts.innerHTML=data.likes
  if (child_p.innerHTML==='like'){child_p.innerHTML='unlike'}

  else if (child_p.innerHTML==='unlike')  {
  child_p.innerHTML= 'like';

 }

  else{
  child_p.innerHTML='like';

  }



});






}

else{
alert(response.error);
}
})
.then(data=>{

})






























   }

   }
}

function editPost(item){

//each item is <a>


item.addEventListener('click', function(){
console.log(item.dataset.id);
if (item.dataset.id === undefined){}
else{


post_id=item.dataset.id;

// to dispaly a form related to specif Edit link and disappear the post body
post_body=document.getElementById(post_id+'div');
post_body.style.visibility = "hidden";
post_txt=document.getElementById(post_id+'p');
post_date=document.getElementById(post_id+'d');

edit_form=document.getElementById(post_id+'form');
edit_form.style.display ='block';
//
//access to TextArea field related to that form
edit_post_body=document.getElementById(post_id+'textarea');

 edit_form.onsubmit= function(){
 let new_post=edit_post_body.value
console.log("from js "+new_post);
fetch(`/EditPost/${post_id}`, {
    method: 'POST',
    body: JSON.stringify({
        body: edit_post_body.value
    })
  })
  .then(response => response.json())
  .then(result => {
      // Print result
      console.log(result);
      if (result.message != null)
      {  console.log("correct");

      // when edit is done correctly it shoud be relaod the profile page
      // i think i should update post_body
edit_form.style.display ='none';
post_body.style.visibility = "visible";



//test here

fetch(`/likePost/${post_id}`)
.then(response => response.json())
.then(data => {
  post_txt.innerHTML=data.post_body;

  post_date.innerHTML=data.date;


});




      }
        if (result.error != null)
      {  console.log("incorrect");}
  });








return false;
    }

}


// call fetch to edit post object in DB






})




}
            });

//function likeEmail(){
//
////post_id=(document.querySelector('button').id);
//alert('post_id');
////fetch(`/likePost/${post_id}`, {
////  method: 'PUT',
////  body: JSON.stringify({
////      like: true
////  })
////})
////.then(response => {ret_resp=response.status;
////
////if (ret_resp==204){
////
////fetch(`/likePost/${post_id}`)
////.then(response => response.json())
////.then(data => {
////
////    console.log(data);
////   document.querySelector('#no_likes').innerHTML=data.likes
////
////
////
////
////
////
////
////
////});
////
////
////
////
////
////
////}
////
////else{
////alert(response.error);
////}
////})
//}