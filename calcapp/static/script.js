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
}

function opClick(ev){
	
	const postObj = {
				 number: parseFloat(actNum),
				 symbol: ev.id.toUpperCase()
			};

	let post = JSON.stringify(postObj);

	disp_to_server(post, url_opclick());
	
	//disable everything until response
	disableButtons(['b0','b1','b2','b3','b4','b5','b6','b7','b8','b9','dc','pl','mi','mu','di','ln','sq','po','clr','equ']);
}

function disableButtons(arr){
	for(let id of arr){
		document.getElementById( id ).disabled = true;
	}
}

function enableButtons(arr){
	for(let id of arr){
		document.getElementById( id ).disabled = false;
	}
}

function refreshData(resp){
	alert(`resp type=${typeof resp} -> content: ${resp} `);
}

function clrClick(){
	//reset number
	let actNum = "";
	decsep_enabled = true;

	disp_to_server(null, url_clear());
}
