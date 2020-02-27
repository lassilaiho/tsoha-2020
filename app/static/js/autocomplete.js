class Autocompleter {
    constructor(endpoint, input, dataList) {
        this._complete = this._complete.bind(this);
        this._endpoint = endpoint;
        this._currentRequest = null;
        this.input = input;
        input.setAttribute("list", dataList.id);
        input.addEventListener("input", this._complete);
        this.dataList = dataList;
        this.completionCount = 10;
    }

    _complete(event) {
        const queryString = event.target.value;
        if (this._currentRequest !== null) {
            this._currentRequest.abort();
        }
        if (!queryString) {
            this._currentRequest = null;
            return;
        }
        this._currentRequest = $.get(this._endpoint, {
            query: queryString,
            count: this.completionCount,
        }, data => {
            this._currentRequest = null;
            const dataList = $(this.dataList).empty();
            for (const completion of data.completions) {
                const option = document.createElement("option");
                option.value = completion;
                dataList.append(option);
            }
        });
    }

    dispose() {
        if (this._currentRequest !== null) {
            this._currentRequest.abort();
            this._currentRequest = null;
        }
        this.dataList = null;
        this.input.removeEventListener("input", this._complete);
        this.input = null;
    }
}
