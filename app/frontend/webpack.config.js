module.exports = {
  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        use: {
          loader: "babel-loader"
        }
      },
      {
        test: /\.(sass|less|css)$/,
	use: [
          'style-loader',
          'css-loader',
          'less-loader'
        ]
      }
    ]
  }
};
