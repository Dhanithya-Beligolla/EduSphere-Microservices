function sendSuccess(res, statusCode, message, data = null) {
  return res.status(statusCode).json({
    success: true,
    message,
    data,
    errors: []
  });
}

function sendError(res, statusCode, message, errors = []) {
  return res.status(statusCode).json({
    success: false,
    message,
    data: null,
    errors
  });
}

module.exports = {
  sendSuccess,
  sendError
};