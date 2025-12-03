let array = [];

const disp = document.getElementById("disp");
const temp = document.getElementById("tempresult");


function calculate(arr) {
    const expression = arr.join("");

    try {
        const result = eval(expression);
        temp.value = result;
    } catch (err) {
        temp.value = "Error";
    }
}
