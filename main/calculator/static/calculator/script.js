function clickButton(button, url, token) {
    var input = document.getElementById("input");
    
    if (button == "C") {
        input.value = "";
    }
    else if (button == "CE") {
        input.value = input.value.slice(0, -1);
    }
    else if (button == "=") {
        fetch( url , {
            method: "post",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": token
            },
            body: input.value
        }).then(function (response) {
            return response.text();
        }).then(function (text) {
            result = JSON.parse(text);
            input.value = result.result;
        }).catch(function (error) {
            console.log(error);
        }
        );

    } else {
        input.value += button;
    }
}