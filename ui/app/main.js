//
// main entry point for app execution
//
// This is determined by the 'entry' option in webpack.config.js
//

import React from 'react'
import ReactDOM from 'react-dom'

import PanelSwitcher from 'components/panel_switcher'
import App from 'app'

class Main extends React.Component {
  render() {
    return React.createElement(PanelSwitcher)
  }

  componentDidMount() {
    App.initialize()
  }
}

ReactDOM.render(
  React.createElement(Main),
  document.getElementById('app')
)
