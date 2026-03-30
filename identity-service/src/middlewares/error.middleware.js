const { sendError } = require('../utils/response');

module.exports = (err, req, res, next) => {
  const statusCode = err.statusCode || 500;
  const message = err.message || 'Internal server error';
  const errors = err.errors || [];

  console.error(err);

  return sendError(res, statusCode, message, errors);
};