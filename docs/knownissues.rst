.. _issues:

===================
Known Issues
===================

VPN
-------------------

* No VPN UI yet.
* Only email is supported, but wizard allows you to login to providers that
  only support VPN.

Wizard
-------------------

* In the wizard log in / sign up page, the username field gets deselected.
* The list of providers should have icons, be sortable, filterable.
* The wizard should look more pretty.

Main window
-------------------

* UI doesn't subscribe to events yet, won't get updated if user has logged out
  via the command line interface.
* Removing an account does not actually clean up all the files associated with
  that account (need backend code).
* Collapsing account list looks weird, and is state is not remembered (need
  backend code).
