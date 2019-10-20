'use strict'

function once (emitter, name) {
  return new Promise((resolve, reject) => {
    const onceError = name === 'error'
    const listener = onceError ? resolve : (...args) => {
      emitter.removeListener('error', error)
      resolve(args)
    }
    emitter.once(name, listener)
    if (onceError) return
    const error = (err) => {
      emitter.removeListener(name, listener)
      reject(err)
    }
    emitter.once('error', error)
  })
}
