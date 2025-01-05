function randomNumber(n: number): number {
    return Math.floor(Math.random() * n);
}

function removeElem<T>(arr: Array<T>, e: any): Array<T> {
    for(let i: number = 0; i < arr.length; i++){
        if (arr[i] === e) {
            var arr1 = arr.slice(0,i);
            var arr2 = arr.slice(i+1,arr.length);
            return(arr1.concat(arr2));
        }
    }
    return(arr);
}

function removeLang(str: string): string {
    var newString: string[] = str.split(" ");
    var result: string[] = [];
    var resstring: string = ""
    for(let i = 0; i < newString.length;i++){
        let tmp: string = newString[i];
        tmp.toLowerCase();
        if(tmp != "language" && tmp != "languages"){
            result.push(tmp);
        }
    }
    for(let j = 0 ; j < result.length; j++){
        resstring += result[j]
    }
    return(resstring)
}

