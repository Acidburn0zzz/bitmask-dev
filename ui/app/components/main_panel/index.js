//
// The main panel manages the current account and the list of available accounts
//
// It displays multiple sections, one for each service.
//

import React from 'react'
import App from 'app'
import Login from 'components/login'
import Account from 'models/account'
import DummyAccount from 'models/dummy_account'

import './main_panel.less'
import AccountList from './account_list'
import UserSection from './user_section'
import EmailSection from './email_section'

export default class MainPanel extends React.Component {

  static get defaultProps() {return{
    initialAccount: null
  }}

  constructor(props) {
    super(props)
    this.state = {
      account: null,
      accounts: []
    }
    this.activateAccount = this.activateAccount.bind(this)
    this.removeAccount = this.removeAccount.bind(this)
  }

  componentWillMount() {
    if (this.props.initialAccount) {
      this.setState({
        account: this.props.initialAccount,
        accounts: Account.list
      })
    }
  }

  activateAccount(account) {
    this.setState({
      account: account,
      accounts: Account.list
    })
  }

  removeAccount(account) {
    Account.remove(account).then(
      newActiveAccount => {
        if (newActiveAccount == null) {
          App.start()
        } else {
          this.setState({
            account: newActiveAccount,
            accounts: Account.list
          })
        }
      },
      error => {
        console.log(error)
      }
    )
  }

  render() {
    let emailSection = null
    let vpnSection = null
    let sidePanel = null

    if (this.state.account.authenticated) {
      if (this.state.account.hasEmail) {
        emailSection = <EmailSection account={this.state.account} />
      }
    }

    sidePanel = (
      <AccountList account={this.state.account}
        accounts={this.state.accounts}
        onSelect={this.activateAccount}
        onRemove={this.removeAccount}/>
    )

    return (
      <div className="main-panel">
        {sidePanel}
        <div className="body">
          <UserSection account={this.state.account} onLogin={this.activateAccount} onLogout={this.activateAccount}/>
          {vpnSection}
          {emailSection}
        </div>
      </div>
    )
  }

}
