var formattedFormData2={};
var occasionValLS;
var cityValLS;


const windowReady = (callBack) => {
    if (document.readyState === 'complete') {
      callBack();
    }
    else {
      window.addEventListener('load', callBack);
    }
};

function setupPalletes(){
	let palettes = sessionStorage.getItem('colorPalettes');
	try {
		palettes = JSON.parse(palettes);
	} catch (error) {
		console.error('Error parsing color palettes:', error);
	}

	const container = document.createElement('div');
	container.className = 'paletteContainer';

	if (Array.isArray(palettes)) {
		palettes.forEach(color => {
			const colorBlock = document.createElement('div');
			colorBlock.style.backgroundColor = color;
			colorBlock.className = 'paletteBlock';
			colorBlock.textContent = color;

			container.appendChild(colorBlock);
		});

		document.querySelector( '.palettes' ).appendChild(container);
	} else {
		console.warn('No valid color palettes found.');
	}
}

windowReady(function () {
	setupPalletes();
	loadInteractivity();
});

function loadInteractivity(){
	$('#Myimg').click(function(){
  		$('#Mymodal').modal('show')
	});
	//const favourites = new Set()
	$('button').click(function(e){
		function msgout(){
			sid=document.getElementById("fav_msg").innerHTML="";

		}
		
		let buttonId=this.id;

		if(buttonId.slice(0,9)=="favourite"){

		sid=document.getElementById("fav_msg").innerHTML="Favourite Added Successfully!"
		setTimeout(msgout, 1000);

		let idx=buttonId.slice(9);
		let imgsrc=document.getElementById("Myimg"+idx).src;
		//favourites.add(imgsrc);

		formattedFormData2["favouriteUrl"]=imgsrc
		occasionValLS=localStorage.getItem("occasionVal");
		cityValLS=localStorage.getItem("cityVal");
		formattedFormData2["occasion"]=occasionValLS
		formattedFormData2["city"]=cityValLS
		formattedFormData2["actionToBePerformed"] = "ADD_NEW_FAVOURITES"
		formData = JSON.stringify(formattedFormData2)
		console.log(formData)
		e.preventDefault();
		$.ajax({
			type:"POST",
            url:"/favourites",
            data:formData,
            success:function(){
				return "success"
                
            },
			dataType: "json",
            contentType : "application/json"
		})
	}else{

		let idx=buttonId.slice(4);
		let imgsrc=document.getElementById("Myimg"+idx).src;
		//console.log(imgsrc)
		formattedFormData2["imageUrl"]=imgsrc
		formData = JSON.stringify(formattedFormData2)
		console.log(formData)
		e.preventDefault();
		$.ajax({
			type:"GET",
            url:"/shopping-results",
            data:formData,
            success:function(){
				return "success"
                
            },
			dataType: "json",
            contentType : "application/json"
		})
	}

	});
	
	
};
