class Observable
{
	constructor()
	{
		this._observers = [];
	}

	register(observer)
	{
		console.log("Subject", this, "gets observed by", observer);
		this._observers.push(observer);
	}

	unregister(observer)
	{
		console.log("Subject", this, "will remove observer", observer);
		rm(this._observers, observer);
	}

	notify(update_function)
	{
		console.log("Subject", this, "sends notifications", update_function, "to", this._observers);
		this._observers.forEach(update_function);
	}
}  
