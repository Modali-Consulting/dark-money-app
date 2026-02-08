<template>
  <div>
    <h1>Investigation Dashboard</h1>
    <div class="grid grid-2">
      <div class="card">
        <h3>Active Pipelines</h3>
        <p>Monitor Bronze → Silver → Gold → Serving health and schedule adherence.</p>
        <ul>
          <li>demo_resources - <span class="badge success">Healthy</span></li>
          <li>demo_finance - <span class="badge warn">Lagging</span></li>
        </ul>
      </div>
      <div class="card">
        <h3>Open Cases</h3>
        <p>Track open hypotheses, targets, and key evidence threads.</p>
        <button>Create Case File</button>
      </div>
    </div>
    <div class="card">
      <h3>Recent Evidence</h3>
      <table class="table">
        <thead>
          <tr>
            <th>Case</th>
            <th>Claim</th>
            <th>Confidence</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>Liberty Advocates Network</td>
            <td>Large transfer to super PAC in Q1</td>
            <td><span class="badge warn">Medium</span></td>
          </tr>
          <tr>
            <td>Citizens for Progress</td>
            <td>Advisor linked to multiple committees</td>
            <td><span class="badge success">High</span></td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>
