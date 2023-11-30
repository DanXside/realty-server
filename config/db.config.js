import { Sequelize } from "sequelize";

export const db = new Sequelize('offers', '', '', {
    host: 'localhost',
    dialect: 'sqlite',
    storage: 'db/realty.db',
    logging: false
});