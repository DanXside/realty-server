import { Realty } from "../models/Realty.js";

export default class RealtyController {
    async getAllRealty (req, res) {
        try {
            const realty = await Realty.findAll();
            if (!realty) {
                return res.status(404).json({message: "Объявления не найдены"})
            }
            res.json({realty})
        } catch (e) {
            console.log(e);
            return res.status(500).json({message: "Не удалось получить объявления"})
        }
    }
    async getOneRealty (req, res) {
        try {
            const realtyId = req.params.id;
            const realty = await Realty.findOne({
                where: {
                    offer_id: Number(realtyId)
                }
            });
            if (!realty) {
                return res.status(404).json({message: "Объявление не найдено"})
            }
            res.json({realty});
        } catch (e) {
            console.log(e);
            return res.status(500).json({message: "Не удалось получить объявление"})
        }
    }
}