import React from 'react'
import Login from './login'
import Center from './center'
import Splash from './splash'
import Area from './area'
import { Glyphicon } from 'react-bootstrap'
import App from 'app'

export default class GreeterPanel extends React.Component {

  constructor(props) {
    super(props)
  }

  newAccount() {
    App.show('wizard')
  }

  onLogin(account) {
    App.start()
  }

  render () {
    return <div>
      <Splash speed="slow" mask={false} />
      <Center width="400">
        <Area position="top" type="light" className="greeter">
          <Login onLogin={this.onLogin.bind(this)}
            rememberAllowed={false} autoAllowed={true} />
        </Area>
        <Area position="bottom" type="dark" className="greeter">
          <Glyphicon glyph="user" />
          &nbsp;
          <a href="javascript:void(0)" onClick={this.newAccount.bind(this)}>Create a new account...</a>
        </Area>
      </Center>
    </div>
  }
}
