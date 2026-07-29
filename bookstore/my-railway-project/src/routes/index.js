const IndexController = require('../controllers/index');

function setRoutes(app) {
    const indexController = new IndexController();

    app.get('/', indexController.getIndex.bind(indexController));
}

module.exports = setRoutes;