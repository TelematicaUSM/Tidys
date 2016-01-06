# COPYRIGHT (c) 2016 Cristóbal Ganter
#
# GNU AFFERO GENERAL PUBLIC LICENSE
#    Version 3, 19 November 2007
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


loading_text = document.getElementById 'loading-text'
promise_num = 0
@load_promise = null
resolveLoadPromise = null

#this could be just an assignment
origHideLoadingFunction = ->
    activatePanels()

hideLoading = origHideLoadingFunction

checkPromiseNum = ->
    if promise_num < 0
        throw new RangeError("The number of promises
                              registered in this module
                              cannot be negative!")

resolvePromise = ->
    promise_num--
    checkPromiseNum()
    unless promise_num
        resolveLoadPromise()
        #@load_promise = null #load_promise stays defined
                              #until next showLoading
                              #invocation
        resolveLoadPromise = null

addPromise = (promise) ->
    promise.then resolvePromise, resolvePromise
    promise_num++
    checkPromiseNum()

@showLoading = (message='Loading ...', promise=null,
                min_time=5000) =>
    unless promise_num
        switchToPanel('loading-panel')
        addPromise(
            new Promise(
                (resolve, reject) ->
                    setTimeout resolve, min_time
            )
        )
        @load_promise = new Promise(
            (resolve, reject) ->
                resolveLoadPromise = resolve
        )
        @load_promise.then(-> hideLoading())

    addPromise promise if promise
    loading_text.innerHTML = message

@setHideLoadingFunction = (func) ->
    hideLoading = func

@resetHideLoadingFunction = ->
    hideLoading = origHideLoadingFunction
