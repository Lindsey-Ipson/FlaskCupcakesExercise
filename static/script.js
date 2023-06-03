const BASE_URL = "http://127.0.0.1:5000/api";


/* Given data about a cupcake, generate html */

function generateCupcakeHTML(cupcake) {
  return `
    <div data-cc-id=${cupcake.id}>
      <li>
        ${cupcake.flavor} | ${cupcake.size} | ${cupcake.rating}
        <button class="delete-button">X</button>
      </li>
      <img class="cupcake-img"
            src="${cupcake.image}"
            alt="(no image provided)">
    </div>
  `;
}


/* Display initial cupcakes on page */

async function showInitialCupcakes() {
  const resp = await axios.get(`${BASE_URL}/cupcakes`);

  for (let cupcakeData of resp.data.cupcakes) {
    let newCupcake = $(generateCupcakeHTML(cupcakeData));
    $("#cupcakes-list").append(newCupcake);
    console.log('NEWCUPCAKE', newCupcake)
  }
}


/* Submit new cupcake when form is submitted and add new cupcake to the page */

$('#new-cupcake-form').on('submit', async function (evt) {
  evt.preventDefault();

  let flavor = $('#form-flavor').val();
  let size = $('#form-size').val();
  let rating = $('#form-rating').val();
  let image = $('#form-image').val();

  console.log('FLAVOR----->', flavor)

  const newCupcakeResp = await axios.post(`${BASE_URL}/cupcakes`, {
    flavor, rating, size, image
  });

  let newCupcake = $(generateCupcakeHTML(newCupcakeResp.data.cupcake));

  $('#cupcakes-list').append(newCupcake);
  $('#new-cupcake-form').trigger('reset')

});


/* Execute showInitialCupcakes function when the document is ready */
$(showInitialCupcakes);