<template>
  <div>
    <h1>Case Files</h1>
    <div class="card">
      <h3>Create a Case</h3>
      <input placeholder="Case title" />
      <textarea placeholder="Hypothesis"></textarea>
      <button>Create</button>
    </div>
    <div class="card">
      <h3>Active Cases</h3>
      <table class="table">
        <thead>
          <tr>
            <th>Title</th>
            <th>Status</th>
            <th>Jurisdictions</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>Liberty Advocates Network</td>
            <td><span class="badge success">Open</span></td>
            <td>US</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>
