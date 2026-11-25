(function(){
const res={data:[],error:null};
const chain=()=>new Proxy(function(){},{get:(t,k)=>k==='then'?(f)=>Promise.resolve(res).then(f):(()=>chain()),apply:()=>chain()});
const user={id:'u1',email:'t@t.t',user_metadata:{full_name:'Test'}};
const session={user,access_token:'x'};
const auth={getSession:async()=>({data:{session},error:null}),getUser:async()=>({data:{user},error:null}),
 onAuthStateChange:(cb)=>({data:{subscription:{unsubscribe(){}}}}),signOut:async()=>({error:null})};
const client={auth,from:()=>chain(),rpc:()=>chain()};
window.supabase={createClient:()=>client};
})();
