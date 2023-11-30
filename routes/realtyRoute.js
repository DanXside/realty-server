import { Router } from "express";
import RealtyController from "../controllers/realtyController.js";


const router = new Router();
const controller = new RealtyController();

router.get('/', controller.getAllRealty);
router.get('/app/:id', controller.getOneRealty);

export default router;