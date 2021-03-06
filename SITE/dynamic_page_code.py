STYLE = """
h1 {
    margin-top: 0;
    margin-bottom: 0;
    text-align: center;
    color: #cccccc;
}
h2 {
    margin-top: 0;
    margin-bottom: 0;
    font-size: 12px;
    text-align: center;
    color: #cccccc;
}
code { 
    font-size: 12px;
    text-align: center;
    color: #cccccc;
}
body {
	background-color: #333333;
}
table {
	text-align: center;
	display: block;
}
th {
	display: block;
	text-align: left;
	color: #cccccc;
}
td {
	display: block;
	text-align: right;
	color: #cccccc;
}
.logline {
	color: #cccccc;
}
.centerimg {
	display: block;
	text-align: center;
	height: 300;
	width: 50%;
	margin-left: auto;
	margin-right: auto;
	color: #eeeeee;
}
margin-right: auto;
}
.shieldimg {
	display: block;
	margin-left: auto;
		margin-right: auto;
}
.shieldrow{
	margin-top: 0;
    text-align: center;
}
.shieldslot{
	margin-top: 0;
    display: inline-block;
}
/* Add a black background color to the top navigation */
.topnav {
	background-color: #333366;
	overflow: hidden;
}

/* Style the links inside the navigation bar */
.topnav a {
	float: left;
	display: block;
	color: #f2f2f2;
	text-align: center;
	padding: 20px 14px;
	text-decoration: none;
	font-size: 17px;
}
/* Change the color of links on hover */
.topnav a:hover {
	background-color: #222222;
	color: white;
}
/* Add an active class to highlight the current page */
.topnav a.active {
	background-color: #4CAF50;
  color: white;
}
/* Hide the link that should open and close the topnav on small screens */
.topnav .icon {
	display: none;
}

.wide_button {
	width: 85%;
	padding: 15px 25px;
	font-size: 24px;
	text-align: center;
	cursor: pointer;
	outline: none;
	color: #fff;
	background-color: #555555;
	border: none;
	border-radius: 15px;
	display: block;
	margin-left: auto;
	margin-right: auto;
}
.wide_button:hover { background-color: #111111 }
.wide_button:active { background-color: #555555 }
.wide_img {
	display: block;
	width: 70%;
	margin-left: auto;
	margin-right: auto;
}
.wide_select {
	display: block;
	width: 85%;
	margin-left: auto;
	margin-right: auto;
}
.centered_label {
	color: #eeeeee;
	font-size: 16px;
	text-align: center;
	display: block;
	margin-left: auto;
	margin-right: auto;
	font-weight: bold;
}
.errortext {
	color: #eeeeee;
	font-size: 12px;
	text-align: left;
	display: block;
	margin-left: auto;
	margin-right: auto;
	font-weight: bold;
}
.errorheader {
	font-size: 16px;
	color: #eeeeee;
	text-align: left;
	display: block;
	margin-left: auto;
	margin-right: auto;
	font-weight: bold;
}
.list_item {
	color: #cccccc;
	text-align: left;
	display: block;
	margin-left: auto;
	margin-right: auto;
}
[type="checkbox"]{
    vertical-align:middle;
}
"""

HOMEPAGE = """<h1>Covid Grapher Web Interface</h1>
<h2>Covid19 metadata provided by covidtracking.com</h2>
<h2>API data licensed under Creative Commons CC BY 4.0.</h2>
<div class="shieldrow">
    <div class="shieldslot"><a href=""><img class="shieldimg" src="https://img.shields.io/badge/License-GPLv3-blue.svg" alt="License"></a></div>
    <div class="shieldslot"><a href=""><img class="shieldimg" src="https://img.shields.io/badge/API%20License-Creative%20Commons%20CC%20BY%204.0-blue" alt="API License"></a></div>
    <div class="shieldslot"><a href=""><img class="shieldimg" src="https://img.shields.io/badge/Language-Python-green" alt="Language"></a></div>
</div>
<img class="centerimg" src="./graph/?region=US&smooth=TRUE&session=53889&key=positiveIncrease" alt="Language">
<br>
"""

COVIDFORM = """
<h1>Covid Grapher API Web Interface</h1>
<h2>Covid19 metadata provided by covidtracking.com</h2>
<h2>API data licensed under Creative Commons CC BY 4.0.</h2>
<br>
<label for="smooth" style="word-wrap:break-word" class="centered_label"> Apply a 7-day rolling average to graph data?
<input type="checkbox" id="smooth" name="smooth" value="True" class="centered_label" />
</label>
<br>
<label class="centered_label" for="data_key">Graph Data Key</label>
<select name='data_key' id='data_key' class = 'wide_select'>
	<option value="positiveIncrease">New Cases</option>
	<option value="hospitalizedCurrently">Hospitalized</option>
	<option value="inIcuCurrently">In ICU</option>
	<option value="onVentilatorCurrently">On Ventilator</option>
	<option value="deathIncrease">Confirmed Deaths</option>
</select>
<br>
<br>
	<label class="centered_label" for="region">
	Regions: (CTRL+Click for multiple regions)
	</label>
</br>
<select name='region' id='region' class='wide_select' size=10 multiple>
	<option value='AL'>AL</option>
	<option value='AK'>AK</option>
	<option value='AZ'>AZ</option>
	<option value='AR'>AR</option>
	<option value='CA'>CA</option>
	<option value='CO'>CO</option>
	<option value='CT'>CT</option>
	<option value='DC'>DC</option>
	<option value='DE'>DE</option>
	<option value='FL'>FL</option>
	<option value='GA'>GA</option>
	<option value='GU'>GU</option>
	<option value='HI'>HI</option>
	<option value='ID'>ID</option>
	<option value='IL'>IL</option>
	<option value='IN'>IN</option>
	<option value='IA'>IA</option>
	<option value='KS'>KS</option>
	<option value='KY'>KY</option>
	<option value='LA'>LA</option>
	<option value='ME'>ME</option>
	<option value='MD'>MD</option>
	<option value='MP'>MP</option>
	<option value='MA'>MA</option>
	<option value='MI'>MI</option>
	<option value='MN'>MN</option>
	<option value='MS'>MS</option>
	<option value='MO'>MO</option>
	<option value='MT'>MT</option>
	<option value='NE'>NE</option>
	<option value='NV'>NV</option>
	<option value='NH'>NH</option>
	<option value='NJ'>NJ</option>
	<option value='NM'>NM</option>
	<option value='NY'>NY</option>
	<option value='NC'>NC</option>
	<option value='ND'>ND</option>
	<option value='OH'>OH</option>
	<option value='OK'>OK</option>
	<option value='OR'>OR</option>
	<option value='PA'>PA</option>
	<option value='PR'>PR</option>
	<option value='RI'>RI</option>
	<option value='SC'>SC</option>
	<option value='SD'>SD</option>
	<option value='TN'>TN</option>
	<option value='TX'>TX</option>
	<option value='US'>US</option>
	<option value='UT'>UT</option>
	<option value='VT'>VT</option>
	<option value='VA'>VA</option>
	<option value='VI'>VI</option>
	<option value='WA'>WA</option>
	<option value='WV'>WV</option>
	<option value='WI'>WI</option>
	<option value='WY'>WY</option>
</select>
<br>
</br>
	<button class = "wide_button" onClick="onClickLoad();"><span>Build Graph</span></button>
<br></br>
<img id="output" class = "wide_img" src="" onerror="imgError(this)" onload="setIntroImage(this)">
"""

COVIDFORMSCRIPT = """
let introImage = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAMgAAABkCAYAAADDhn8LAAABhWlDQ1BJQ0MgcHJvZmlsZQAAKJF9kT1Iw0AcxV9bpVorDnYQcchQnVoQFREnqWIRLJS2QqsOJpd+QZOGJMXFUXAtOPixWHVwcdbVwVUQBD9AnBydFF2kxP8lhRYxHhz34929x907wNuoMMXoGgcU1dRT8ZiQza0K/lf0IYBezCIiMkNLpBczcB1f9/Dw9S7Ks9zP/Tn65bzBAI9APMc03STeIJ7eNDXO+8QhVhJl4nPiiE4XJH7kuuTwG+eizV6eGdIzqXniELFQ7GCpg1lJV4iniMOyolK+N+uwzHmLs1KpsdY9+QuDeXUlzXWaI4hjCQkkIUBCDWVUYCJKq0qKgRTtx1z8w7Y/SS6JXGUwciygCgWi7Qf/g9/dGoXJCScpGAO6XyzrYxTw7wLNumV9H1tW8wTwPQNXattfbQAzn6TX21r4CBjYBi6u25q0B1zuAENPmqiLtuSj6S0UgPcz+qYcMHgLBNac3lr7OH0AMtTV8g1wcAiMFSl73eXdPZ29/Xum1d8P09ByznMBbqYAAAAGYktHRAAOAF4AXqyCelcAAAAJcEhZcwAALiMAAC4jAXilP3YAAAAHdElNRQfkCwoKAzfHa1FbAAAAGXRFWHRDb21tZW50AENyZWF0ZWQgd2l0aCBHSU1QV4EOFwAACdlJREFUeNrtnXuMHVUdxz/dbkq7VAtCW2gLPiig1rZgV1BLQ6E0UQNC5RGCVWKIKVRNoNRnKjZITRAVFA2PKFYkusa2kEIrCiXGIlQXkacWaChS+qDQdumydrtd9/rH/Cb3t5M7987r7vP7SW7u3DNnzpw55/zO+Z0zM98LQgghhBBCCCGEEEIIIYQQQgghhBBCCCGEEEIIIYQQQgghhBBCCCGEEEIk4B6gBBzoo/P92c5XAj5qYatc2NQax79t8bYMoTpIc/19XV+9aKgQdoPLfPj5H/AmsBY4a5BXzi77fj3BNbcDG4GFg+j6jgNuAp4G3gIOAjuAJ4BbgdOHQH31q4F4vm1xTgA2A+cBG4DPDwED2RWz/5t2ze8F/gOcAfwauCjj+eYCI+yzqc7XtgD4N7AUeMM6s3HAfBvJFgErhlh9hSx3ndsFfWUg2AlfAa613yMGYSGnLfAS8KoZRsinB/h1fRhoAQ630eKTwJNAJ/C8Gc05wN4haiD9MoJ4nnXbU4AjKviTHwPuBF4D1rj4JwMrgW1AF7AfeBz4QuQco4Arbd9ucw92Aq3AZRni5S3wkW57p9t+2F3zMTHhR2fwt+cDj1mj3mNl1piwfm6wcsE6sEMV4vwFuCRmLlCp7r4IPGPuzUH7vAr8BvhglXnFEuBRu4Z2M9yjY/I9xa5zD7APuBeYnLK+WoDvuN/3Wj7aXNhHgNV2LYfse42Fp8L748tc+AQX3uUqwxfMW277Pts/B+iwz3ygCbjCxfuqO8d6C9tnE9rDgBnAbcCNGeJlueZvmGGcDDxnYdsilZbXQCqFzbN5T8ka6gTgfTY5rTVJb7I6KQE9wDszTJYr1d2NwC1WFqNtlHrelf3EmLSWAUcCZ1pnWAIerGJMRwDNbkHiTxnqsJqLdZ4ZRQm4ysrnWvt9CDi3CAP5hAtfHXOxn3MjSzhCbbF9v4qcZ7uFb7XfH3DpPFQlf0njZb3mSp+bIo2uaANpAF6033td55N0Feskl97+jKtJ0bqL4yp3zOUJVqZWuvCZNeI+6ox8dEEG0uja2kuRY150HeDIrC5WA/B+4HtuNWFJTNzHI8PaTJvgYxN73+gmWXjYwMIeDPOVW4GfmRvmh+ek8bISTtLHABdbZS211axRdXJ1pwMnujLsKshtvr2CsW9KWHfhfPNC4G6b17wG/NjtT2JQmyPtoRpt7ryTCirbU11aT0X2Pe3cvBlZDOS7Nuw/B4y3oX+Wre4k4Vi3fYdbzfGfMbZ/h/XkIc3AYuAu83vPTxkvDyWbB6xyDWoG8Kk6GcgEt/1mhuO3A922fbi5N9g8bYS5tllYa2Ww0EbrBcCXIgZUiw63PbFG3O6M8+OkZft2ZF+72x6fdZl3hA1Tx9ky4fYUmfOVfWKC+NcB04BvAb935xoDfD9DvCLYW6GCe1I2kqQrNWEDT0uHTcBDzi4gT6c73/x3NrK2kv6G3VFuu573Mkox4burjHhNMfF6+Wf15ElrvJNtwna89fKeWcA/3O9/2SdcrWq37zGR45LGy8u73fY/3SgWcmRkhSsLW8x1HGfubBaWWxmPtLnjOhsFs+LnXDtypDPHvrsKnDNWc8+wRRtfZzvMzYqWbbN9b7PVulzLvFnotrlBp1VcC/Aha8inENxn+LnFnWsFeLH11IeZ/xv6/TenjJeX0TYhnW6/7wH+btsPuHiXA2OB2dYBZOEA8APbnmarfONs4px0srrRlmW7rGwfNoNpipuA1qCV4GZjuEAznuDm6dIEx060MllM+cmLFQV0JNV4xI0iFzkD7zZXs9sM5BrgHcDVNj8+ZJ5RT95VrCQrIVOrrLLcDrxgjaHTrHoD8GWLM9V6vZetN+2y0eZ+gptepIyXdxWrx0alJ8xQop3J12wFrtNGwAtyLvM2ANdbIzpgZXWNuU9pnsU6CfgpwR31Dspr/httNe6MFHXXbCtLndbA/gb80B1zdUxad1vZHLTrWJSwzdxH8ntGlbjEJt4H7Lq3un2nEdz32G3Xstt+NyNEH7AqZ+MekDSoXoWQgQghhBBCCCGEEEIIIYQQQoi+YTl1EBgQxaMbhUIMYBYQPDXaSfDI8W2U3xiMPpyXVPjBPxM0l+qCAFnTzSNw0ELl13rbMuSpEmmEFipRj/K7zqX5FRe+1IUviMnD9OFqHBe6QghFCk6gskhBGuGHNIIAWdPNK3BQzcVKk6dKpMlHLQMpqvxOdWG/dcdvcOG3uvBt9NYrGHaMInjcPYlIQRrhh2gFVxMEyJNuXoGDOANJm6ekxOWjloEUWX5how9f1x5ro1t4rvDlt0ku7CfDdQ5yCuX31WuJFKQRfqhGVBAgT7r1Ejgo4lqLyEc9yi98yex4c9PmWcf4B+C/BGo1x9JbGvX+4Wog73Lbb9SIm0b4oRpRQYCi0g0pQuCgiDwVkY96lJ9v7LMpv9y2muBtQMxoQgPZTyCX2q809tN52yLuVjXSCj8kpch0KwkchBPYSpTqlKe0+ejL8nvERoom4ONmICUCEcBGy/fZBK/1AvyRyuqQw2IEeZayOkatyguFH6As/BBlVoY8FJluWoGDOIGBvHkqSmihHuXXSVm04TKL/xTBK8brLfwcyq/A9rt71Z8G0kEg9oatslxhlXspZZGCkhvakwo/pHUZiko3rcBBNYGBPHnKI7TQF+UXNvpQg2qdm8A/QyAtNZZAi23dcDYQgK8T6G69YsayyQqup0Iv+5BNCu8g0FlqNR91vU0If5ExD0Wl20YgKvdXm7jutAazocoIeqk1inMJ7jNsLSBPafORl7R5XRdxL9dH9oU8xuBToe8TJg+kJT4h+pPPEizxzbZheRLBXemS9ajvURGJ4cw8As3ffbZa0U6goXQX5fV1IYQQQgghhBBCCCHEUGBIikYPFPTKrRAyECFkIELIQPqBpMISRYk6RNNaQvC66x6Cpw1aiP+76ynUFlkQojDSCEsUKerg01pG8EehZxI8KVsCHqxiTNVEFoQojDTCEtGGmlfUIW5laqULn1kjblRkQWSgUUUQSxphiShxog6fAc43l+oYev/JfRKD2uy2ZxL8YWUcUZGFl1WlMpAiSSMskYS1BC9HlczdWmNGeKdryLXocNu19K26NdeUgdSTNMIStShKTOEot/26qqj+qGeJJ42wRC2KElOYY99dlAUQ0nCLm68sVBXLQPKQRliiFnnEFCYSCBksBs6ysBUE75sLGUi/kkZYopa7llVMYZGNZjcDLwFXAterasRApS+EJfQAokaQQUElYYlQhXwv8CMVkQxkOLOLQMzsAZuTvABMA34JnGaulxBCCCGEEEIIIYQQQgghhBBCCCGEEEIIIYQQQgghhBBCCCGEEEIIIYQQwvN/rQAUkAnJZBAAAAAASUVORK5CYII="
let errorImage = "data:image/png;base64,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"
let loadingImage = "data:image/png;base64,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"
function getRandomInt(max) {
	return Math.floor(Math.random() * Math.floor(max));
}
function getSelectedOptions(sel) {
    var opts = [], opt;
    for (var i=0, len=sel.options.length; i<len; i++) {
        opt = sel.options[i];
        if ( opt.selected ) { opts.push(opt.value) }
    }
    return opts;
}
function RemoveLastChunkOfURL(url) {
	console.log(url)
	url = url.trim("/");
	var path_chunks = url.split('/');		
	var new_path = "";
	for (i = 0; i < path_chunks.length - 1; i++) {
	  new_path += path_chunks[i];
	  new_path += "/";
	}
	console.log(new_path)
	return new_path;
}
function buildGraph() {
	document.getElementById("output").src = loadingImage;
	var url = "/graph/?";
	var regions = getSelectedOptions(document.getElementById("region"));
	var opts = [], opt;
	if ( regions.length > 0 ) {
		url += "region="
		for (var i=0, len=regions.length; i<len; i++) {
	        opt = regions[i];
	        url += opt;
	        if (i < len - 1){
	        	url +="+";
	        }
	    }
	} else { url += "region=US" }
	var smooth = document.getElementById("smooth").checked;
	if ( smooth ){
		url += "&smooth=TRUE";
	} else {
		url += "&smooth=FALSE";
	}
	// Random session value to prevent caching issues
	url += "&session=" + getRandomInt(99999)
	var sel = document.getElementById("data_key");
	var datakey = sel.options[sel.selectedIndex].value;
	url += "&key=" + datakey;
	console.log("Getting graph from " + url);
	return url;
}
function imgError(image) {
    image.onerror = "";
    image.src = errorImage;
    return true;
}
function setIntroImage(image) {
	image.onload = "";
    image.src = introImage;
    return true;
}
function onClickLoad() { document.getElementById("output").src = buildGraph() }

function onResize() {
	let landscape = true;
	if(window.innerHeight > window.innerWidth){
		landscape = false;
	    alert("Please use Landscape!");
	}
}
"""