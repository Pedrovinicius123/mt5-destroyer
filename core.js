const tf = require('@tensorflow/tfjs')
const fs = require('fs');
const path = require('path');

require('./modules/express')

const model = tf.sequential()

try {
    const jsonCode = fs.readFileSync('model.json', 'utf-8');
    let obj = JSON.parse(jsonCode);
    const loadedModel = tf.sequential(modelJson);
    console.log(loadedModel)
}

catch (err){
    console.log('File not existent yet');
}

const inputSize = 30;  // Tamanho do seu conjunto de entrada
const hiddenLayerSize = 128;  // Número de unidades na camada oculta
const outputSize = 2;  // Número de classes de saída


model.add(tf.layers.dense({ inputShape: [inputSize], units: hiddenLayerSize, activation: 'linear' }));
model.add(tf.layers.dense({ units: hiddenLayerSize, activation: 'linear'}))
model.add(tf.layers.dense({units: hiddenLayerSize, activation: 'linear'}))
model.add(tf.layers.dense({ units: outputSize, activation: 'softmax' }));

const parameters = {
    
    optimizer: 'sgd',
    loss: 'meanSquaredError',
    metrics : ['accuracy']

}

model.compile(parameters)

const epochs = 1000;
const learningRate = 0.1;

const xs = tf.tensor2d([], [5, 1]);
const ys = tf.tensor2d([], [4, 1]);

let idx0 = 0
let idx1 = 30

async function train(xs, ys){
    for (let epoch = 0; epoch < epochs; epoch++){

        const response = await model.fit(xs, ys, {
            epochs: 1,
            shuffle: true,
            batchSize: 4,
            learningRate: learningRate
        })
    
        idx0 += 30
        idx1 += 30

    }
}

const JSONmodel = JSON.stringify(model.toJSON())

fs.writeFile('model.json', JSONmodel, (err)=>{
    if (err){
        console.log(err)
    }
})
