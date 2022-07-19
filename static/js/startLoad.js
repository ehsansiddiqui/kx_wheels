// JavaScript Document
		function startKXLoad() {
    		document.getElementById('loadBox').style.left = '50%';
			document.getElementById('loadBox').style.top = '50%';
			document.getElementById('loadBox').style.marginLeft = '-200px';
			document.getElementById('loadBox').style.marginTop = '-118px';

			document.getElementById('loadBorder').style.left = '0px';
			document.getElementById('loadBorder').style.top = '0px';
			document.getElementById('loadBorder').style.right = '0px';
			document.getElementById('loadBorder').style.bottom = '0px';
		}
		
		
		function endKXLoad() {
    		document.getElementById('loadBox').style.left = '-1000px';
			document.getElementById('loadBox').style.top = '-1000px';
			document.getElementById('loadBox').style.marginLeft = '-1000px';
			document.getElementById('loadBox').style.marginTop = '-1000px';

			document.getElementById('loadBorder').style.left = '-1000px';
			document.getElementById('loadBorder').style.top = '-1000px';
			document.getElementById('loadBorder').style.right = 'auto';
			document.getElementById('loadBorder').style.bottom = 'auto';
		}