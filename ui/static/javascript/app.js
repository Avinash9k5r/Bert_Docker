
const main_url = 'localhost' //make the ec2 url change here, just put the url inside quotes.

//#######################################################################################################################


const charactersList = document.getElementById('charactersList');
const searchBar = document.getElementById('searchBar');
let hpCharacters = [];

searchBar.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        const searchString = e.target.value.toLowerCase();
        if (searchString == ''){
            searchString = 'nousrinp' // any random non existent word, for handing the case when no user-input is provided.
        }
        console.log(searchString)
        function httpGet(theUrl) {
            var xmlHttp = new XMLHttpRequest();
            xmlHttp.open("GET", theUrl, false);
            xmlHttp.send();
            return xmlHttp.responseText;
        }

        window.location.href="http://"+ main_url +":5000/search?input="+searchString
      }

    // const filteredCharacters = hpCharacters.filter((character) => {
    //     return (
    //         character.name.toLowerCase().includes(searchString) ||
    //         character.house.toLowerCase().includes(searchString)
    //     );
    // });
    // displayCharacters(filteredCharacters);
});


document.getElementById("microphone").addEventListener("click", myFunction);

function myFunction() {


    alert("MICROPHONE USAGE DEPRECIATED\nUSE KEYBOARD INSTEAD!!");


    // function httpGet(theUrl) {
    //     var xmlHttp = new XMLHttpRequest();
    //     xmlHttp.open("GET", theUrl, false);
    //     xmlHttp.send();
    //     return xmlHttp.responseText;
    // }

    // window.location.href="http://ec2-44-192-4-254.compute-1.amazonaws.com:5000/converter_stt"

}
