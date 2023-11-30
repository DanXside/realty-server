import express from 'express';
import 'dotenv/config';
import { db } from './config/db.config.js';
import realtyRouter from './routes/realtyRoute.js';

const app = express();

db.sync().then(() => {
    console.log('connection to db')
});

app.use(express.json());
app.use('/realty', realtyRouter);

const start = async () => {
    try {
        app.listen(process.env.PORT, () => {
            console.log(`Server work on port ${process.env.PORT}`);
        })
    } catch (e) {
        console.log(e);
    }
}

start();