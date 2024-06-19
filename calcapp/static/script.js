let actNum = "";
decsep_enabled = true;

function numClick(ev){
	if(ev.id == "dc"){
		if(decsep_enabled){
			decsep_enabled = false;
			actNum = actNum + ".";
		}
	} else {
		actNum = actNum + ev.id.substr(1);
	}
	console.log(actNum)
	document.getElementById( 'result' ).innerHTML = actNum;
}

function opClick(ev){
	
	const postObj = {
				 number: actNum,
				 symbol: ev.id.toUpperCase()
			};

	let post = JSON.stringify(postObj);

	disp_to_server(post, url_opclick());
	
	//disable everything until response
	disableButtons(['b0','b1','b2','b3','b4','b5','b6','b7','b8','b9','dc','pl','mi','mu','di','ln','sq','po','clr','equ']);
}

function disableButtons(arr){
	for(let id of arr){
		try{
			document.getElementById( id ).disabled = true;
		} catch (err) {
			console.log(`disableButtons :: no such ID in Document: ${id}`);
		}
	}
}

function enableButtons(arr){
	for(let id of arr){
		try{
			document.getElementById( id ).disabled = false;
		} catch (err) {
			console.log(`enableButtons :: no such ID in Document: ${id}`);
		}
	}
}

function refreshData(resp){
	//alert(`resp type=${typeof resp} -> content: ${resp} `);
	//console.log(`resp :: ${Object.entries(resp)}`);
	
	let en = [], di = [], robj = JSON.parse(resp);
	for(const [key, value] of Object.entries(robj)){
		if(key != 'RESULT' && key != 'EXPRESSION' && key != 'STATE' ){
			if(value){
				en.push( key.toLowerCase() );
			} else {
				di.push( key.toLowerCase() );
			}
		} else {
			let v = value || "";
			if(v=="undefined"){
				v="";
			}
			document.getElementById( key.toLowerCase() ).innerHTML = v;
		}
	}
	
	enableButtons( en );
	disableButtons( di );
	
	let an = null;
	try{
		an = Float.parse(resp.RESULT);
	} catch(err) {
		actNum = "";
	} finally {
		if(an==null){
			actNum = "";
		} else {
			actNum = resp.RESULT;
		}
	}
	
}

function clrClick(){
	//reset calculator
	console.log("forget everything")
	let actNum = "";
	decsep_enabled = true;

	disp_to_server(null, url_clear());
}
