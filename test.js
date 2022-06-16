

let prom = new Promise((resolve, reject) => {
    let a = 1 + 1;
    if (a == 2) {
        resolve('s')
    }
    else {
        reject('failed')
    }
})

prom.then((messege) => {
    console.log('mes')
}).catch()