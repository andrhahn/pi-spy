module.exports.auth = function (req, res, next) {
  console.log(`x-user-name header: ${req.header('x-user-name')}`);
  console.log(`x-user-pw header: ${req.header('x-user-pw')}`);

  const user_name = req.header('x-user-name');
  const user_pw = req.header('x-user-pw');

  if (user_name === 'foo' && user_pw === 'bar') {
    next()
  } else {
    res.status(401).json({message: 'invalid credentials'})
  }
};
